import { useCallback, useState } from 'react';
import { observer } from 'mobx-react';
import { useHistory } from 'react-router-dom';
import { useToggle } from 'react-use';
import Modal from 'react-modal';
import { useStore } from '../../../stores';
import { formatCurrency } from '../../../lib/currency-helpers';

import deleteRound from '@cfpb/cfpb-icons/src/icons/delete-round.svg';

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
    (id) => (evt) => {
      evt.preventDefault();
      history.push(`/calendar/add/${id}/edit`);
    },
    []
  );

  const title = uiStore.selectedDate ? uiStore.selectedDate.toFormat('DDD') : uiStore.currentMonth.toFormat('MMMM, y');
  const events = uiStore.selectedDate
    ? eventStore.eventsByDate.get(uiStore.selectedDate.startOf('day').valueOf())
    : eventStore.eventsByMonth.get(uiStore.currentMonth.startOf('month').valueOf());
  const balance = uiStore.selectedDate
    ? eventStore.getBalanceForDate(uiStore.selectedDate)
    : eventStore.getBalanceForDate(uiStore.currentMonth.endOf('month'));

  return (
    <div className="calendar-details">
      <h2>Transactions for {title}</h2>

      <ul className="calendar-details__events">
        {events &&
          events.map((e) => (
            <li className="calendar-details__event" key={e.id} role="button" onClick={editEvent(e.id)}>
              <div className="calendar-details__event-date">{e.dateTime.toFormat('D')}</div>
              <div className="calendar-details__event-name">{e.name}</div>
              <div className="calendar-details__event-total">{formatCurrency(e.total)}</div>
              <button className="calendar-details__event-delete" onClick={confirmDelete(e)}>
                <span dangerouslySetInnerHTML={{ __html: deleteRound }} />
              </button>
            </li>
          ))}
      </ul>

      <div className="calendar-details__total">
        <strong className="calendar-details__total-label">Total Balance:</strong>
        <span className="calendar-details__total-value">{formatCurrency(balance || 0)}</span>
      </div>

      <Modal
        className="modal-dialog"
        contentLabel="Event deletion options"
        isOpen={modalOpen}
        onRequestClose={() => toggleModal(false)}
        appElement={document.querySelector('#mmt-my-money-calendar')}
        closeTimeoutMS={150}
        overlayClassName="modal-overlay"
        id="delete-dialog"
      >
        <p className="modal-dialog__prompt">Delete this event?</p>
        <ul className="modal-dialog__actions">
          <li className="modal-dialog__action">
            <button tabIndex="0" className="modal-dialog__action-button" onClick={eventDeleteHandler(false)}>
              {eventRecurs ? 'Just this event' : 'Delete'}
            </button>
          </li>
          {eventRecurs && (
            <li className="modal-dialog__action">
              <button tabIndex="1" className="modal-dialog__action-button" onClick={eventDeleteHandler(true)}>
                This event and future recurrences
              </button>
            </li>
          )}
          <li className="modal-dialog__action">
            <button
              tabIndex="2"
              className="modal-dialog__action-button modal-dialog__action-button--cancel"
              onClick={() => toggleModal(false)}
            >
              Cancel
            </button>
          </li>
        </ul>
      </Modal>
    </div>
  );
}

export default observer(Details);
