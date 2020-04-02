import { observer } from 'mobx-react';
import { useStore } from '../../stores';
import { CardGroup, Card } from '../../components/card';

import idea from '@cfpb/cfpb-icons/src/icons/idea-round.svg';

function FixItStrategies() {
  const { strategyStore } = useStore();

  return (
    <section className="strategies">
      <header className="strategies-header">
        <h2 className="strategies-header__title">Fix-It Strategies</h2>

        <p className="strategies-header__intro">
          This week you went into the red. Below are the transactions you made. Explore the different strategies that can prevent going into the red in the future.
        </p>
      </header>

      <main className="strategies-cards">
        <CardGroup columns={2}>
          <Card title="Foo" icon={idea}>
            Blah Blah
          </Card>
        </CardGroup>
      </main>
    </section>
  );
}

export default observer(FixItStrategies);
