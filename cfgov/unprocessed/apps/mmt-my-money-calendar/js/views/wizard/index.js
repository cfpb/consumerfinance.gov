import { Route, Redirect, Switch, Link, useRouteMatch } from "react-router-dom";
import Step from "./step";

export default function Wizard() {
  const match = useRouteMatch("/wizard/step/:step");

  return (
    <section className="wizard">
      <div>This is the Wizard Index Page</div>
      <h1>New User Wizard</h1>

      <Link to="/">Back Home</Link>

      <h3>Route match debug</h3>
      <pre className="debug">{JSON.stringify(match, null, 2)}</pre>

      <Switch>
        <Redirect exact from="/wizard" to="/wizard/step/1" />
        <Route path="/wizard/step/:step">
          <Step />
        </Route>
      </Switch>
      <Link to="/summary">Go to Summary</Link>
    </section>
  );
}
