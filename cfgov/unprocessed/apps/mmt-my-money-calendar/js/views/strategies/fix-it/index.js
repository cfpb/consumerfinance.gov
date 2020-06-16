import { useEffect, useCallback } from 'react';
import { observer } from 'mobx-react';
import { useHistory, useParams } from 'react-router-dom';
import { useStore } from '../../../stores';
import { CardGroup, Card } from '../../../components/card';
import { useScrollToTop } from '../../../components/scroll-to-top';
import { dayjs } from '../../../lib/calendar-helpers';
import { Button, ButtonLink } from '../../../components/button';

import { pencil, arrowLeft, ideaRound } from '../../../lib/icons';

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
    <Button icon={pencil} onClick={buttonAction} variant="secondary">
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
            <FixItButton result={result} />
          </div>
        </Card>
      ))}
    </CardGroup>
  </main>
);

function FixItStrategies() {
  const { uiStore, strategiesStore: strategies } = useStore();
  const { week } = useParams();

  useEffect(() => {
    if (!uiStore.currentWeek && !week) {
      uiStore.setCurrentWeek(dayjs());
      return;
    }

    const weekInt = Number(week);

    if (weekInt && weekInt !== uiStore.currentWeek.valueOf()) uiStore.setCurrentWeek(dayjs(weekInt));
  }, []);

  useScrollToTop();

  return (
    <section className="strategies">
      <header className="strategies-header">
        <h2 className="strategies-header__title">Fix-It Strategies</h2>

        {strategies.fixItResults.length ? (
          <div className="strategy-cards">
            <CardGroup columns={2}>
              <div className="fixit-header">
                <div className="fixit-header__line-first">
                  <div>
                    Amount that puts you in{' '}
                    <strong>
                      <em>RED</em>
                    </strong>
                    :
                  </div>
                  <div className="fixit-header__amount">{uiStore.weekEndingBalanceText}</div>
                </div>

                <div className="fixit-header__line">
                  The amount that puts you in{' '}
                  <strong>
                    <em>RED</em>
                  </strong>{' '}
                  is what you should try to reduce.
                </div>
              </div>
              <div className="fixit-header">
                <div className="fixit-header__comment">
                  <div>Weekly Starting Balance:</div>
                  <div className="fixit-header__comment-value">{uiStore.weekStartingBalanceText}</div>
                </div>
                <div className="fixit-header__comment">
                  <div>Total Weekly Income: </div>
                  <div className="fixit-header__comment-value">$300</div>
                </div>
                <div className="fixit-header__comment">
                  <div>Total Weekly Expense:</div>
                  <div className="fixit-header__comment-value"> -$500</div>
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

      {strategies.fixItResults.length > 0 && <StrategyCards results={strategies.fixItResults} />}

      <footer className="strategies-footer">
        <ButtonLink iconSide="left" icon={arrowLeft} to="/calendar">
          Back to Calendar
        </ButtonLink>
      </footer>
    </section>
  );
}

export default observer(FixItStrategies);
