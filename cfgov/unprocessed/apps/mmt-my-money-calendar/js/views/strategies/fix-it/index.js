import { useEffect, useCallback, useState } from 'react';
import { observer } from 'mobx-react';
import { useHistory, useParams } from 'react-router-dom';
import { useStore } from '../../../stores';
import { CardGroup, Card } from '../../../components/card';
import { useScrollToTop } from '../../../components/scroll-to-top';
import { formatCurrency } from '../../../lib/currency-helpers';
import { dayjs } from '../../../lib/calendar-helpers';
import { Button, ButtonLink } from '../../../components/button';
import Strategies from '../index';

import { pencil, arrowLeft, ideaRound } from '../../../lib/icons';
import NarrativeModal from '../../../components/narrative-notification';
import { narrativeCopy } from '../../../lib/narrative-copy';

const FixItButton = ({ result }) => {
  const href = result.event ? `/calendar/add/${result.event.id}/edit` : result.link.href;
  const label = result.event ? `Edit ${result.event.categoryDetails.name}` : result.link.text;
  const { eventStore } = useStore();
  const history = useHistory();
  const buttonAction = useCallback(
    async (evt) => {
      evt.preventDefault();

      // Hide "Split Payment" fix-it strategies for this event once the user clicks Fix It once
      if (result.event && result.event.category.includes('housing')) {
        result.event.setHideFixItStrategy(true);
        await eventStore.saveEvent(result.event, true);
      }

      history.push(href);
    },
    [result.event, href]
  );

  return (
    <Button icon={pencil} onClick={buttonAction} variant="strategy">
      {label}
    </Button>
  );
};

const StrategyCards = ({ results }) => (
  <main className="strategies-cards">
    <CardGroup columns={2}>
      {results.map((result, index) => (
        <Card title={result.title} icon={ideaRound} key={`strategy-${index}`}>
          <p>{result.text}</p>
          <div className="m-card_footer">
            {result.title === 'Explore Your General Strategies' ? null : <FixItButton result={result} />}
          </div>
        </Card>
      ))}
    </CardGroup>
  </main>
);

function FixItStrategies() {
  const { uiStore, eventStore, strategiesStore: strategies } = useStore();
  const { week } = useParams();
  const [showModal, setShowModal] = useState();

  const handleModalSession = () => {
    let fixItVisit = localStorage.getItem('fixItVisit');

    if (fixItVisit) {
      setShowModal(false);
    } else {
      setShowModal(true);
    }
  };

  useEffect(() => {
    if (!uiStore.currentWeek && !week) {
      uiStore.setCurrentWeek(dayjs());
      return;
    }

    const weekInt = Number(week);

    if (weekInt && weekInt !== uiStore.currentWeek.valueOf()) uiStore.setCurrentWeek(dayjs(weekInt));
    handleModalSession()
  }, []);

  const handleToggleModal = (event) => {
    event.preventDefault();
    localStorage.setItem('fixItVisit', true);
    setShowModal(!showModal);
  };

  useScrollToTop();

  const events = eventStore.getPositiveEventsForWeek(uiStore.currentWeek) || [];
  var positiveFilter = events.filter((event) => event.total > 0);
  var initialBalance = positiveFilter.find((event) => event.category === 'income.startingBalance');
  var positiveEvents = positiveFilter.filter((event) => (event.category !== 'income.startingBalance' && event.category !== 'income.benefits.snap'));
  var weekIncome = positiveEvents.reduce((acc, event) => acc + event.total, 0);
  var negativeFilter = events.filter((event) => event.total < 0);
  var weekExpenses = negativeFilter.reduce((acc, event) => acc + event.total, 0);
  return (
    <section className="strategies">
      {showModal && (
        <NarrativeModal showModal={showModal}
                        handleOkClick={handleToggleModal}
                        copy={narrativeCopy.step3} />
      )}
      <header className="strategies-header">
        <h2 className="strategies-header__title">Fix-It Strategies</h2>
        {strategies.fixItResults.length ? (
          <div className="strategy-cards">
            <h3 className="strategies-header__week-range">Week of {uiStore.weekRangeText}</h3>
            <CardGroup columns={2}>
              <div className="fixit-header">
                <div className="fixit-header__line-first">
                  <div>Amount that you went over: </div>
                  <div className="fixit-header__amount">{uiStore.weekEndingBalanceText}</div>
                </div>

                <div className="fixit-header__line">
                  The amount you went over is what you should try to reduce. The strategies below can help.
                </div>
              </div>
              <div className="fixit-header">
                <div className="fixit-header__comment">
                  <div>Starting Balance:</div>
                  <div className="fixit-header__comment-value">{initialBalance ? formatCurrency(initialBalance.total) : uiStore.weekStartingBalanceText}</div>
                </div>
                <div className="fixit-header__comment">
                  <div>Income: </div>
                  <div className="fixit-header__comment-value">{formatCurrency(weekIncome)}</div>
                </div>
                <div className="fixit-header__comment">
                  <div>Expense:</div>
                  <div className="fixit-header__comment-value">{formatCurrency(weekExpenses)}</div>
                </div>
              </div>
              <div className="fixit-header">
                <div className="fixit-header__comment">
                  <div>You currently have a SNAP balance of {uiStore.weekEndingSnapBalanceText}.</div>
                </div>
              </div>
            </CardGroup>
          </div>
        ) : (
            <p>
              <em>There are no strategy recommendations for this week</em>
            </p>
          )}
      </header>
      <div>{strategies.fixItResults.length > 0 && <StrategyCards results={strategies.fixItResults} />}</div>
      <div>
        <Strategies />
      </div>

      <footer className="strategies-footer">
        <ButtonLink iconSide="left" icon={arrowLeft} to="/calendar">
          Back to Calendar
        </ButtonLink>
      </footer>
    </section>
  );
}

export default observer(FixItStrategies);
