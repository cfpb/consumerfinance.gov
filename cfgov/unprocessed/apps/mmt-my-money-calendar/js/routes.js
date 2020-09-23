import { Redirect, Route, BrowserRouter as Router, Switch } from 'react-router-dom';
import Home from './views/home';
import Calendar from './views/calendar/index';
import AddEvent from './views/calendar/add';
import BottomNav from './components/bottom-nav';
import FixItStrategies from './views/strategies/fix-it';
import Strategies from './views/strategies';
import MoneyOnHand from './views/money-on-hand';
import More from './views/more';
import Export from './views/more/export';

const Routes = () => <Router basename='/mmt-my-money-calendar'>
  <div className='app'>
    <Switch>
      <Route exact path='/'>
        <Home />
      </Route>

      <Route path='/money-on-hand'>
        <MoneyOnHand />
      </Route>

      <Route exact path='/calendar'>
        <Calendar />
      </Route>

      <Route path='/calendar/add'>
        <AddEvent />
      </Route>

      <Route path='/fix-it-strategies/:week'>
        <FixItStrategies />
      </Route>

      <Route path='/fix-it-strategies'>
        <FixItStrategies />
      </Route>

      <Route path='/strategies'>
        <Strategies />
      </Route>

      <Route exact path='/more/export'>
        <Redirect to='/more' />
      </Route>

      <Route exact path='/more/export/:dataType'>
        <Export />
      </Route>

      <Route exact path='/more'>
        <More />
      </Route>
    </Switch>

    <BottomNav />
  </div>
</Router>;
export default Routes;
