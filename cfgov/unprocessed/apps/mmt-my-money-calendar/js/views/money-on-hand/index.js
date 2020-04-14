import { Route, Switch, withRouter } from 'react-router-dom';
import { useStore } from '../../stores';
import { useBEM } from '../../lib/hooks';
import Start from './start';

function MoneyOnHand({ match }) {
  return (
    <Switch>
      <Route path={match.path}>
        <Start />
      </Route>
    </Switch>
  );
}

export default withRouter(MoneyOnHand);
