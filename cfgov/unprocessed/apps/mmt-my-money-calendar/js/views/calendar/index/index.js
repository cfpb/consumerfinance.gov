import clsx from 'clsx';
import { useEffect, useMemo, useState } from 'react';
import { useLocation, useParams, Redirect } from 'react-router-dom';
import { observer } from 'mobx-react';
import { useStore } from '../../../stores';
import { useClickHandler, useClickConfirm } from '../../../lib/hooks';
import Day from './day';
import Details from './details';
import NarrativeModal from '../../../components/narrative-notification';
import { useScrollToTop } from '../../../components/scroll-to-top';
import { DAY_LABELS, dayjs } from '../../../lib/calendar-helpers';
import { narrativeCopy } from '../../../lib/narrative-copy';

import { arrowLeft, arrowRight, downArrow } from '../../../lib/icons';

const IconButton = ({ icon, ...props }) => <button dangerouslySetInnerHTML={{ __html: icon }} {...props} />;

const CalendarWeekRow = ({ days, selected }) => {
  const classes = clsx('calendar__row', selected && 'selected');

  return (
    <div className={classes}>
      {days.map((day) => (
        <Day day={day} key={`day-${day.dayOfYear()}`} />
      ))}
    </div>
  );
};

function Calendar() {
  const { uiStore, eventStore } = useStore();
  const location = useLocation();
  const params = useParams();
  const [showModal, setShowModal] = useState();
  const [narrativeStep, setNarrativeStep] = useState();

  const handleModalSession = () => {
    let visited = localStorage.getItem('visitedPage'),
        enteredData = localStorage.getItem('enteredData');

    if (visited && enteredData === 'subsequent') {
      setShowModal(false);
    } else {
      let currentStep = (visited && enteredData === 'initial') ? 'step2' : 'step1';

      setNarrativeStep(currentStep)
      setShowModal(true);
    }
  }

  useEffect(() => {
    uiStore.setPageTitle('myMoney Calendar');
    uiStore.setSubtitle(uiStore.currentMonth.format('MMMM YYYY'));
    handleModalSession()
  }, [location, params, uiStore.currentMonth]);

  const dayLabels = useMemo(
    () => (
      <div className="calendar__row" key="dayLabels">
        {DAY_LABELS.map((label, idx) => (
          <div key={`label-${idx}`} className="calendar__day-label">
            {label}
          </div>
        ))}
      </div>
    ),
    []
  );

  const handleToggleModal = (event) => {
    event.preventDefault();
    localStorage.setItem('visitedPage', true);
    if (localStorage.getItem('enteredData') === 'initial') {
      localStorage.setItem('enteredData', 'subsequent');
    }
    if (!localStorage.getItem('removeSpotlight')) {
      localStorage.setItem('removeSpotlight', true)
      eventStore.closeNarrativeModal()
    }
    setShowModal(!showModal);
  };

  useScrollToTop();

  if (eventStore.eventsLoaded && !eventStore.hasStartingBalance) return <Redirect to="/money-on-hand" />;

  return (
    <section className="calendar">
      {showModal && narrativeStep === 'step1' &&
        <NarrativeModal showModal={showModal}
                        handleOkClick={handleToggleModal}
                        copy={narrativeCopy.step1}
                        step={narrativeStep}
        />
      }
      { showModal && narrativeStep === 'step2' &&
        <NarrativeModal showModal={showModal}
                        handleOkClick={handleToggleModal}
                        copy={narrativeCopy.step2}
                        step={narrativeStep}
        />
      }
      <header className="calendar__header">
        <IconButton
          className="calendar__nav-button"
          aria-label="Previous Month"
          onClick={() => uiStore.prevMonth()}
          icon={arrowLeft}
        />

        <h2 className="calendar__subtitle">{uiStore.subtitle}</h2>

        <IconButton
          className="calendar__nav-button"
          aria-label="Next Month"
          onClick={() => uiStore.nextMonth()}
          icon={arrowRight}
        />
      </header>

      <div className="calendar__cols">
        <div className="calendar__rows">
          {[
            dayLabels,
            ...uiStore.monthCalendarRows.map(({ days, weekNumber }) => (
              <CalendarWeekRow
                days={days}
                key={`week-${weekNumber}`}
                selected={uiStore.currentWeek.week() === weekNumber}
              />
            )),
          ]}
        </div>

        <Details />
      </div>
    </section>
  );
}

export default observer(Calendar);
