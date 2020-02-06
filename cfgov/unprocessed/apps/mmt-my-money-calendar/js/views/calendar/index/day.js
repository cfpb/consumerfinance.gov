import clsx from 'clsx';
import { useMemo, useCallback } from 'react';
import { observer } from 'mobx-react';
import { DateTime } from 'luxon';
import { useStore } from '../../../stores';
import { compact } from '../../../lib/array-helpers';

import addRound from '@cfpb/cfpb-icons/src/icons/add-round.svg';
import subtractRound from '@cfpb/cfpb-icons/src/icons/subtract-round.svg';

const Icon = ({ icon, size, style = {}, ...props }) => {
  const styles = {
    width: `${size}px`,
    height: `${size}px`,
    ...style,
  };

  return <span className="calendar__day-icon" style={styles} dangerouslySetInnerHTML={{ __html: icon }} {...props} />;
};

function Day({ day, dateFormat = 'd' }) {
  const { uiStore, eventStore } = useStore();

  const isToday = useMemo(() => day.hasSame(DateTime.local(), 'day'), [day]);
  const isSelected = useMemo(() => uiStore.selectedDate && day.hasSame(uiStore.selectedDate, 'day'), [
    day,
    uiStore.selectedDate,
  ]);
  const isCurrentMonth = useMemo(() => day.hasSame(uiStore.currentMonth, 'month'), [day, uiStore.currentMonth]);
  const dateString = useMemo(() => day.toFormat(dateFormat), [day, dateFormat]);

  const classes = ['calendar__day', isToday && 'today', isSelected && 'selected', isCurrentMonth && 'current-month'];

  const handleClick = useCallback(
    (evt) => {
      evt.preventDefault();

      uiStore.selectedDate && day.equals(uiStore.selectedDate)
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
    []
  );

  if (!eventStore.events.length) return emptyTile();

  const balance = eventStore.getBalanceForDate(day);

  classes.push({
    'pos-balance': balance > 0,
    'neg-balance': balance < 0,
  });

  const symbols = compact([
    eventStore.dateHasIncome(day) && <Icon icon={addRound} key="add-icon" size={20} />,
    eventStore.dateHasExpenses(day) && <Icon icon={subtractRound} key="subtract-icon" size={20} />,
  ]);

  return (
    <div className={clsx(classes)} role="button" onClick={handleClick}>
      <div className="calendar__day-number">
        <time dateTime={day.toFormat('y-MM-dd')} className="calendar__day-datetime">
          {day.toFormat(dateFormat)}
        </time>
      </div>
      <div className="calendar__day-symbols">{symbols}</div>
    </div>
  );
}

export default observer(Day);
