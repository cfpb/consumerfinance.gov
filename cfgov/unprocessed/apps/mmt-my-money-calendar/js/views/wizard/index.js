import { Route, Redirect, Switch, Link, useRouteMatch } from "react-router-dom";
import StartingBalance from "./steps/starting-balance";
import Income from "./steps/income";
import Expenses from "./steps/expenses";

export default function Wizard() {
  const match = useRouteMatch("/wizard/steps/:step");
  const { step } = match.params;

  return (
    <section className="wizard">
      <div>This is the Wizard Index Page</div>
      <h1>New User Wizard</h1>

      <Link to="/">Back Home</Link>

      <h3>Route match debug</h3>
      <pre className="debug">{JSON.stringify(match, null, 2)}</pre>

      <Switch>
        {/* <Redirect exact from="/wizard" to="/wizard/steps/starting-balance" /> */}

        <Route path="/wizard/steps/starting-balance">
          <StartingBalance />
        </Route>
        <Route path="/wizard/steps/income">
          <Income />
        </Route>
        <Route path="/wizard/steps/expenses">
          <Expenses />
        </Route>
      </Switch>

      {/* <div className="step-nav"> */}
      {/* If step is greater than 1, show back button */}
      {/* {step > 1 && <Link to={`/wizard/steps/${step - 1}`}>Back</Link>} */}

      {/* If step is less than 3, show continue button */}
      {/* {step < 3 && <Link to={`/wizard/steps/${step + 1}`}>Continue</Link>} */}
      {/* </div> */}

      <Link to="/summary">Go to Summary</Link>
    </section>
  );
}
