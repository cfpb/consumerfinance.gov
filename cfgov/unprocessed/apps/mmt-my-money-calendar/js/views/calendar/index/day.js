import clsx from 'clsx';
import { useMemo, useCallback } from 'react';
import { observer } from 'mobx-react';
import { useStore } from '../../../stores';
import { dayjs } from '../../../lib/calendar-helpers';

const Icon = ({ icon, size, style = {}, ...props }) => {
  const styles = {
    width: `${size}px`,
    height: `${size}px`,
    ...style,
  };

  return <span className="calendar__day-icon" style={styles} dangerouslySetInnerHTML={{ __html: icon }} {...props} />;
};

function Day({ day, dateFormat = 'D' }) {
  const { uiStore, eventStore } = useStore();

  const isToday = day.dayOfYear() === dayjs().dayOfYear();
  const isSelected = uiStore.selectedDate && day.isSame(uiStore.selectedDate, 'day');
  const isCurrentMonth = day.isSame(uiStore.currentMonth, 'month') && day.isSame(uiStore.currentMonth, 'year');
  const dateString = day.format(dateFormat);

  const classes = ['calendar__day', isToday && 'today', isSelected && 'selected', isCurrentMonth && 'current-month'];

  const handleClick = useCallback(
    (evt) => {
      evt.preventDefault();

      uiStore.selectedDate && day.isSame(uiStore.selectedDate)
        ? uiStore.clearSelectedDate()
        : uiStore.setSelectedDate(day);
    },
    [day]
  );

  const emptyTile = useCallback(
    () => (
      <div className={clsx(classes)} role="button" onClick={handleClick}>
        <div className="calendar__day-number">{dateString}</div>
        <div className="calendar__day-symbols" />
      </div>
    ),
    [dateString]
  );

  if (!eventStore.events.length) return emptyTile();

  const balance = eventStore.getBalanceForDate(day);

  classes.push({
    'pos-balance': balance > 0,
    'neg-balance': balance < 0,
  });

  const symbol = eventStore.dateHasEvents(day) ? <div className="calendar__day-symbols">&bull;</div> : null;

  return (
    <div className={clsx(classes)} role="button" onClick={handleClick}>
      <div className="calendar__day-number">
        <time dateTime={day.format('YYYY-MM-DD')} className="calendar__day-datetime">
          {day.format(dateFormat)}
        </time>
      </div>
      {symbol}
    </div>
  );
}

export default observer(Day);
