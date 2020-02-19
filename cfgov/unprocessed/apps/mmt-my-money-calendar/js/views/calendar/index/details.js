import { observer } from 'mobx-react';
import { useStore } from '../../../stores';
import { formatCurrency } from '../../../lib/currency-helpers';

import deleteRound from '@cfpb/cfpb-icons/src/icons/delete-round.svg';

function Details() {
  const { uiStore, eventStore } = useStore();

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
            <li className="calendar-details__event" key={e.id}>
              <div className="calendar-details__event-date">{e.dateTime.toFormat('D')}</div>
              <div className="calendar-details__event-name">{e.name}</div>
              <div className="calendar-details__event-total">{formatCurrency(e.total)}</div>
              <button className="calendar-details__event-delete" onClick={() => eventStore.deleteEvent(e.id)}>
                <span dangerouslySetInnerHTML={{__html: deleteRound}} />
              </button>
            </li>
          ))}
      </ul>

      <div className="calendar-details__total">
        <strong className="calendar-details__total-label">Total Balance:</strong>
        <span className="calendar-details__total-value">{formatCurrency(balance || 0)}</span>
      </div>
    </div>
  );
}

export default observer(Details);
