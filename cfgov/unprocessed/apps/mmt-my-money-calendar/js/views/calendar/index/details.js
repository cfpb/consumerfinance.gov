import clsx from 'clsx';
import { useCallback, useState } from 'react';
import { useLockBodyScroll, useKeyPressEvent } from 'react-use';
import { observer } from 'mobx-react';
import { useHistory, Link } from 'react-router-dom';
import { useToggle } from 'react-use';
import Modal from 'react-modal';
import { useStore } from '../../../stores';
import { formatCurrency } from '../../../lib/currency-helpers';
import { Notification } from '../../../components/notification';
import { SlideListItem } from '../../../components/slide-list';
import ModalDialog from '../../../components/modal-dialog';

import pencil from '@cfpb/cfpb-icons/src/icons/pencil.svg';
import deleteIcon from '@cfpb/cfpb-icons/src/icons/delete.svg';
import arrowRight from '@cfpb/cfpb-icons/src/icons/arrow-right.svg';
import arrowLeft from '@cfpb/cfpb-icons/src/icons/arrow-left.svg';

const IconButton = ({ icon, ...props }) => <button dangerouslySetInnerHTML={{ __html: icon }} {...props} />;

const DetailRow = ({ event, onRequestEdit, onRequestDelete, ...props }) => (
  <SlideListItem
    className="calendar-details__event"
    actions={[
      {
        label: 'Edit',
        icon: pencil,
        className: 'slide-list-item__button--edit',
        onClick: onRequestEdit,
      },
      {
        label: 'Delete',
        icon: deleteIcon,
        className: 'slide-list-item__button--delete',
        onClick: onRequestDelete,
        disabled: event.category === 'startingBalance',
      },
    ]}
    {...props}
  >
    <div className="calendar-details__event-date">{event.dateTime.format('M/D/YYYY')}</div>
    <div className="calendar-details__event-name">{event.name}</div>
    <div className="calendar-details__event-total">{formatCurrency(event.total)}</div>
  </SlideListItem>
);

function Details() {
  const { uiStore, eventStore } = useStore();
  const history = useHistory();
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [modalOpen, toggleModal] = useToggle(false);

  const confirmDelete = useCallback(
    (event) => (e) => {
      e.preventDefault();
      e.stopPropagation();
      setSelectedEvent(event);
      toggleModal(true);
    },
    []
  );

  const eventDeleteHandler = useCallback(
    (andRecurrences = false) => async (evt) => {
      evt.preventDefault();
      await eventStore.deleteEvent(selectedEvent.id, andRecurrences);
      setSelectedEvent(null);
      toggleModal(false);
    },
    [selectedEvent]
  );

  const eventRecurs = selectedEvent && selectedEvent.recurs;

  const editEvent = useCallback(
    (e) => (evt) => {
      evt.preventDefault();
      history.push(`/calendar/add/${e.id}/edit`);
    },
    []
  );

  useKeyPressEvent('ArrowRight', uiStore.nextWeek.bind(uiStore));
  useKeyPressEvent('ArrowLeft', uiStore.prevWeek.bind(uiStore));

  useLockBodyScroll(modalOpen);

  const events = eventStore.eventsByWeek.get(uiStore.currentWeek.startOf('week').valueOf());
  const income = events ? events.filter(({ totalCents }) => totalCents > 0) : [];
  const expenses = events ? events.filter(({ totalCents }) => totalCents < 0) : [];
  const endBalanceClasses = clsx('calendar-details__ending-balance', uiStore.weekHasNegativeBalance && 'negative');

  return (
    <section className="calendar-details">
      <header className="calendar-details__header">
        <IconButton
          className="calendar-details__nav-button"
          aria-label="Previous Week"
          onClick={() => uiStore.prevWeek()}
          icon={arrowLeft}
        />

        <div className="calendar-details__header-text">
          <h3>{uiStore.weekRangeText}</h3>
          <div className="calendar-details__starting-balance">
            Week starting balance: {uiStore.weekStartingBalanceText}
          </div>
          {!uiStore.weekHasNegativeBalance && (
            <div className={endBalanceClasses}>Week ending balance: {uiStore.weekEndingBalanceText}</div>
          )}
        </div>

        <IconButton
          className="calendar-details__nav-button"
          aria-label="Next Week"
          onClick={() => uiStore.nextWeek()}
          icon={arrowRight}
        />
      </header>

      {uiStore.weekHasNegativeBalance && (
        <div className={endBalanceClasses}>
          <Notification
            message="You're in the red!"
            variant="error"
            actionLink={
              <Link to="/strategies" className="m-notification_button">
                Fix it
              </Link>
            }
          >
            <p className="m-notification_explanation">Week ending balance: {uiStore.weekEndingBalanceText}</p>
          </Notification>
        </div>
      )}

      <div className="calendar-details__events-section">
        <h3 className="calendar-details__events-section-title">Income</h3>

        <ul className="calendar-details__events-list">
          {income.map((e) => (
            <DetailRow event={e} onRequestEdit={editEvent(e)} onRequestDelete={confirmDelete(e)} key={e.id} />
          ))}
        </ul>
      </div>

      <div className="calendar-details__events-section">
        <h3 className="calendar-details__events-section-title">Expenses</h3>

        <ul className="calendar-details__events-list">
          {expenses.map((e) => (
            <DetailRow event={e} onRequestEdit={editEvent(e)} onRequestDelete={confirmDelete(e)} key={e.id} />
          ))}
        </ul>
      </div>

      <ModalDialog
        contentLabel="Event deletion options"
        isOpen={modalOpen}
        onRequestClose={() => toggleModal(false)}
        id="delete-dialog"
        prompt="Delete this event?"
        actions={[
          {
            label: eventRecurs ? 'Just this event' : 'Delete',
            onClick: eventDeleteHandler(false),
          },
          {
            label: 'This event and future recurrences',
            onClick: eventDeleteHandler(true),
            condition: eventRecurs,
          },
        ]}
        showCancel
      />
    </section>
  );
}

export default observer(Details);
