import { observer } from 'mobx-react';
import { useStore } from '../../stores';
import { useScrollToTop } from '../../components/scroll-to-top';
import { CardGroup, Card } from '../../components/card';

const StrategyCards = ({ results }) => (
  <main className="strategy-cards">
    <CardGroup columns={2}>
      {results.map((result, index) => (
        <Card title={result.title} icon={result.icon1} key={`strategy-${index}`}>
          <p>{result.body}</p>

          {!!result.link && (
            <div className="m-card_footer">
              <a href={result.link.href} className="a-btn a-btn__full-on-xs" target="_blank">
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
      {strategiesStore.strategyResults.length > 0 && <StrategyCards results={strategiesStore.strategyResults} />}
    </section>
  );
}

export default observer(Strategies);
