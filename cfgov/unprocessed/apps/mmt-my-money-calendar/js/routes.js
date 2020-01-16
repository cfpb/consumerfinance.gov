import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import Home from "./views/home";
import StartingBalance from "./views/wizard/steps/starting-balance";
import Income from "./views/wizard/steps/income";
import Expenses from "./views/wizard/steps/expenses";
import Summary from "./views/summary";

const Routes = () => (
  <Router basename="/mmt-my-money-calendar">
    test
    <div className="app">
      <Switch>
        <Route exact path="/">
          <Home />
        </Route>

        <Route path="/wizard/steps/starting-balance">
          <StartingBalance />
        </Route>

        <Route path="/wizard/steps/income">
          <Income />
        </Route>

        <Route path="/wizard/steps/expenses">
          <Expenses />
        </Route>

        <Route path="/summary">
          <Summary />
        </Route>
      </Switch>
    </div>
  </Router>
);

export default Routes;
