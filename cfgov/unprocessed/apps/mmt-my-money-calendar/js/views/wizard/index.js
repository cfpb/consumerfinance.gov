import { Route, Redirect, Switch, Link, useRouteMatch } from "react-router-dom";
import StartingBalance from "./steps/starting-balance";
import Income from "./steps/income";
import Expenses from "./steps/expenses";

export default function Wizard() {

  return (
    <section className="wizard">
      <div>This is the Wizard Index Page</div>
      <h1>New User Wizard</h1>

      <Link to="/">Back Home</Link>

      <Switch>
        <Route path="/wizard/starting-balance">
          <StartingBalance />
        </Route>
        <Route path="/wizard/income">
          <Income />
        </Route>
        <Route path="/wizard/expenses">
          <Expenses />
        </Route>
      </Switch>

      <Link to="/summary">Go to Summary</Link>
    </section>
  );
}
