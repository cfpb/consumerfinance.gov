import { useEffect, useCallback } from 'react';
import { useLocation, useParams } from 'react-router-dom';
import { observer } from 'mobx-react';
import { useStore } from '../../stores';
import Day from './day';
import Button from '../../components/button';

import arrowRight from 'cf-icons/src/icons/arrow-right.svg';
import arrowLeft from 'cf-icons/src/icons/arrow-left.svg';

const CalendarWeekRow = ({ days }) => (
  <div className="calendar__row">
    {days.map((day) => <Day day={day} key={`day-${day.toFormat('ooo')}`} />)}
  </div>
);

function Calendar() {
  const { uiStore, } = useStore();
  const location = useLocation();
  const params = useParams();

  const nextMonth = useCallback((evt) => {
    evt.preventDefault();
    uiStore.nextMonth();
  }, [uiStore.currentMonth]);

  const prevMonth = useCallback((evt) => {
    evt.preventDefault();
    uiStore.prevMonth();
  }, [uiStore.currentMonth]);

  useEffect(() => {
    uiStore.setPageTitle('myMoney Calendar');
    uiStore.setSubtitle(uiStore.currentMonth.toFormat('MMMM, y'));
  }, [location, params, uiStore.currentMonth]);

  return (
    <section className="calendar">
      <h1>{uiStore.pageTitle}</h1>
      <h2>{uiStore.subtitle}</h2>

      <nav className="calendar__nav">
        <Button icon={arrowLeft} iconSide="left" onClick={prevMonth}>
          Previous
        </Button>
        <Button icon={arrowRight} iconSide="right" onClick={nextMonth}>
          Next
        </Button>
      </nav>

      <div className="calendar__rows">
        {uiStore.monthCalendarRows.map(({ days, weekNumber }) => <CalendarWeekRow days={days} key={`week-${weekNumber}`} />)}
      </div>
    </section>
  );
}

export default observer(Calendar);
