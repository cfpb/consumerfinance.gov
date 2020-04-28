import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import Home from './views/home';
import Calendar from './views/calendar/index';
import AddEvent from './views/calendar/add';
import BottomNav from './components/bottom-nav';
import FixItStrategies from './views/strategies/fix-it';
import Strategies from './views/strategies';
import MoneyOnHand from './views/money-on-hand';
import More from './views/more';

const Routes = () => (
  <Router basename="/mmt-my-money-calendar">
    <div className="app">
      <Switch>
        <Route exact path="/">
          <Home />
        </Route>

        <Route path="/money-on-hand">
          <MoneyOnHand />
        </Route>

        <Route exact path="/calendar">
          <Calendar />
        </Route>

        <Route path="/calendar/add">
          <AddEvent />
        </Route>

        <Route path="/fix-it-strategies/:week">
          <FixItStrategies />
        </Route>

        <Route path="/fix-it-strategies">
          <FixItStrategies />
        </Route>

        <Route path="/strategies">
          <Strategies />
        </Route>

        <Route path="/more">
          <More />
        </Route>
      </Switch>

      <BottomNav />
    </div>
  </Router>
);

export default Routes;
