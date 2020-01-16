import { Route, Redirect, Switch, Link, useRouteMatch } from "react-router-dom";
import Interval from "./interval";

export default function Summary() {
  const match = useRouteMatch("/summary/interval/:interval");

  return (
    <section id="summary-view">
      <h1>Summary Screen</h1>

      <Link to="/">Back Home</Link>

      <h3>Route match debug</h3>
      <pre className="debug">{JSON.stringify(match, null, 2)}</pre>
      <Switch>
        <Redirect exact from="/summary" to="/summary/interval/1" />
        <Route path="/interval/:interval">
          <Interval />
        </Route>
      </Switch>
    </section>
  );
}
