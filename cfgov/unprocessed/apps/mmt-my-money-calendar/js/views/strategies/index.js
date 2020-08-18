import { observer } from 'mobx-react';
import { useStore } from '../../stores';
import { useScrollToTop } from '../../components/scroll-to-top';
import { CardGroup, Card } from '../../components/card';
import { ButtonLink } from '../../components/button';

const StrategyCards = ({ results }) => (
  <main className="strategy-cards">
    <CardGroup columns={2}>
      {results.map((result, index) => (
        <Card title={result.title} key={`strategy-${index}`}>
          <p>{result.body}</p>

          {!!result.link && (
            <div className="m-card_footer">
              <a href={result.link.href} className="a-btn a-btn__secondary a-btn__full-on-xs" target="_blank">
                {result.link.text}
              </a>
            </div>
          )}
        </Card>
      ))}
    </CardGroup>
  </main>
);

function Strategies() {
  const { strategiesStore } = useStore();

  useScrollToTop();

  return (
    <section className="strategies">
      {/* <header className="strategies-header">
        <h2 className="strategies-header__title">General Strategies to Improve Cash Flow</h2>

        <p className="strategies-header__intro">
          The strategies below are tailored to the specific expenses and income in your budget. Commit to implementing
          one or two of them for the coming month and see if your cash flow improves.
        </p>
      </header> */}
      {strategiesStore.strategyResults.length > 0 && <StrategyCards results={strategiesStore.strategyResults} />}
    </section>
  );
}

export default observer(Strategies);
