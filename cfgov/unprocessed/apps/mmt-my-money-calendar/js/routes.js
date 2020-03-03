import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import Home from './views/home';
import Wizard from './views/wizard';
import Summary from './views/summary';
import Calendar from './views/calendar/index';
import AddEvent from './views/calendar/add';
import BottomNav from './components/bottom-nav';

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

        <Route path="/summary">
          <Summary />
        </Route>

        <Route exact path="/calendar">
          <Calendar />
        </Route>

        <Route path="/calendar/add">
          <AddEvent />
        </Route>
      </Switch>

      <BottomNav />
    </div>
  </Router>
);

export default Routes;
