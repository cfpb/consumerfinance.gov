import clsx from 'clsx';
import { dayjs } from '../../../lib/calendar-helpers';
import { observer } from 'mobx-react';
import { useCallback } from 'react';
import { useStore } from '../../../stores';


function Day( { day, dateFormat = 'D' } ) {
  const { uiStore, eventStore } = useStore();

  const isToday = day.dayOfYear() === dayjs().dayOfYear();
  const isSelected = uiStore.selectedDate && day.isSame( uiStore.selectedDate, 'day' );
  const isCurrentMonth = day.isSame( uiStore.currentMonth, 'month' ) && day.isSame( uiStore.currentMonth, 'year' );
  const dateString = day.format( dateFormat );

  const classes = [ 'calendar__day', isToday && 'today', isSelected && 'selected', isCurrentMonth && 'current-month' ];

  const handleClick = useCallback(
    evt => {
      evt.preventDefault();
      if ( uiStore.selectedDate && day.isSame( uiStore.selectedDate ) ) {
        uiStore.clearSelectedDate();
      } else {
        uiStore.setSelectedDate( day );
      }
    },
    [ day ]
  );

  const emptyTile = useCallback(
    klass => <div className={clsx( klass )} role='button' onClick={handleClick}>
      <div className='calendar__day-number'>{dateString}</div>
      <div className='calendar__day-symbols' />
    </div>
    ,
    [ dateString ]
  );

  if ( !eventStore.events.length ) return emptyTile( classes );

  const weekEndBal = eventStore.getDay( day.endOf( 'week' ) ).nonSnapBalance;

  classes.push( {
    'pos-balance':
      weekEndBal >= 0 &&
      ( dayjs( day ).startOf( 'week' ) || dayjs( day ).isBetween( dayjs( day ).startOf( 'week' ), dayjs( day ).endOf( 'week' ) ) ),
    'neg-balance':
      weekEndBal < 0 &&
      ( dayjs( day ).startOf( 'week' ) || dayjs( day ).isBetween( dayjs( day ).startOf( 'week' ), dayjs( day ).endOf( 'week' ) ) )
  } );

  const symbol = eventStore.dateHasEvents( day ) ? <div className='calendar__day-symbols'>&bull;</div> : null;

  return (
    <div className={clsx( classes )} role='button' onClick={handleClick}>
      <div className='calendar__day-number'>
        <time dateTime={day.format( 'YYYY-MM-DD' )} className='calendar__day-datetime'>
          {day.format( dateFormat )}
        </time>
      </div>
      {symbol}
    </div>
  );
}

export default observer( Day );
