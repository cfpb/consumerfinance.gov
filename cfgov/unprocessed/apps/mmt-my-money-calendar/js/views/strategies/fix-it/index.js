import { useEffect } from 'react';
import { observer } from 'mobx-react';
import { Link, Redirect, useParams } from 'react-router-dom';
import { useStore } from '../../../stores';
import { CardGroup, Card } from '../../../components/card';
import { useScrollToTop } from '../../../components/scroll-to-top';
import { dayjs } from '../../../lib/calendar-helpers';
import { ButtonLink } from '../../../components/button';

import { pencil, arrowLeft, ideaRound } from '../../../lib/icons';

const StrategyCards = ({ results }) => (
  <main className="strategies-cards">
    <CardGroup columns={2}>
      {results.map((result, index) => (
        <Card title={result.title} icon={ideaRound} key={`strategy-${index}`}>
          <p>{result.text}</p>

          <div className="m-card_footer">
            {result.event ? (
              <ButtonLink icon={pencil} to={`/calendar/add/${result.event.id}/edit`} variant="secondary">
                Edit {result.event.categoryDetails.name}
              </ButtonLink>
            ) : (
              <ButtonLink icon={pencil} to={result.link.href} variant="secondary">
                {result.link.text}
              </ButtonLink>
            )}
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
          <p className="strategies-header__intro">
            This week the total cost of your expenses was more than your income, putting you into the red. The
            strategies below are tailored to the specific expenses in your budget for the week. Commit to implementing
            one or two of them to prevent from going into the red in the future.
          </p>
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
