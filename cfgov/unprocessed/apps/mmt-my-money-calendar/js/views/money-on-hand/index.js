import { Route, Switch, Redirect, withRouter } from 'react-router-dom';
import { useStore } from '../../stores';
import { useBEM } from '../../lib/hooks';
import Start from './start';
import Sources from './sources';
import BalanceForm from './balance-form';
import Summary from './summary';

function MoneyOnHand({ match }) {
  const { eventStore } = useStore();
  const bem = useBEM('wizard');

  if (eventStore.eventsLoaded && eventStore.events.length) return <Redirect to="/calendar" />;

  return (
    <section className="wizard">
      <Switch>
        <Route path={`${match.path}/sources`}>
          <Sources />
        </Route>

        <Route path={`${match.path}/balances/:source`}>
          <BalanceForm />
        </Route>

        <Route exact path={`${match.path}/balances`}>
          <BalanceForm />
        </Route>

        <Route path={`${match.path}/summary`}>
          <Summary />
        </Route>

        <Route path={match.path}>
          <Start />
        </Route>
      </Switch>
    </section>
  );
}

export default withRouter(MoneyOnHand);
