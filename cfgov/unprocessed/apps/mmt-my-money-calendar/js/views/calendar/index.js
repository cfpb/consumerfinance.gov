import { useEffect } from 'react';
import { useLocation, useParams } from 'react-router-dom';
import { observer } from 'mobx-react';
import { useStore } from '../../stores';
import Day from './day';

const CalendarWeekRow = ({ days }) => (
  <div className="calendar__row">
    {days.map((day) => <Day day={day} key={`day-${day.toFormat('ooo')}`} />)}
  </div>
);

function Calendar() {
  const { uiStore, } = useStore();
  const location = useLocation();
  const params = useParams();

  useEffect(() => {
    uiStore.setPageTitle('myMoney Calendar');
    uiStore.setSubtitle(uiStore.currentMonth.get('monthLong'));
  }, [location, params]);

  return (
    <section className="calendar">
      <h1>{uiStore.pageTitle}</h1>
      <h2>{uiStore.subtitle}</h2>

      <div className="calendar__rows">
        {uiStore.monthCalendarRows.map(({ days, weekNumber }) => <CalendarWeekRow days={days} key={`week-${weekNumber}`} />)}
      </div>
    </section>
  );
}

export default observer(Calendar);
