import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import Home from './views/home';
import Wizard from './views/wizard';

const Routes = () => (
  <Router basename="/mmt-my-money-calendar">
    <div className="app">
      <Switch>
        <Route exact path="/">
          <Home />
        </Route>

        <Route path="/wizard">
          <Wizard />
        </Route>
      </Switch>
    </div>
  </Router>
);

export default Routes;
