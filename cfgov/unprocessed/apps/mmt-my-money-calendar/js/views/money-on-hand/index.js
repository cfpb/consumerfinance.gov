import { Route, Switch, Redirect, withRouter } from 'react-router-dom';
import { useStore } from '../../stores';
import { useBEM } from '../../lib/hooks';
import Start from './start';

function MoneyOnHand({ match }) {
  const { eventStore } = useStore();

  if (eventStore.eventsLoaded && eventStore.events.length) {
    return <Redirect to="/calendar" />;
  }

  return (
    <Switch>
      <Route path={match.path}>
        <Start />
      </Route>
    </Switch>
  );
}

export default withRouter(MoneyOnHand);
