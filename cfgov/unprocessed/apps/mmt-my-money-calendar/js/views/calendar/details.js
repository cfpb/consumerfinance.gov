import { useMemo } from 'react';
import { observer } from 'mobx-react';
import { useStore } from '../../stores';
import { formatCurrency } from '../../lib/currency-helpers';

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
              {e.name}: {formatCurrency(e.total)}
            </li>
          ))}
      </ul>

      <div className="calendar-details__total">
        <strong>Your Balance:</strong> {formatCurrency(balance)}
      </div>
    </div>
  );
}

export default observer(Details);
