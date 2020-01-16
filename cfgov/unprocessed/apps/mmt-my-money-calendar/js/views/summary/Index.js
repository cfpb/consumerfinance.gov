import React from "react";
import { Route, Redirect, Switch, Link, useRouteMatch } from "react-router-dom";

import { Month } from "./Month";

export default function Summary() {
  return (
    <section id="summary-view">
      <h1>Here is your Summary Screen</h1>
      <Link to="/">Back Home</Link>

      <h3>Route match debug</h3>
      <pre className="debug">{JSON.stringify(match, null, 2)}</pre>
      <Switch>
        <Redirect exact from="/summary" to="/summary/month" />
        <Route path="/summary/:interval">
          <Interval />
        </Route>
      </Switch>
      <Month />
      <div className="strategy">Strategy List Link</div>
    </section>
  );
}
