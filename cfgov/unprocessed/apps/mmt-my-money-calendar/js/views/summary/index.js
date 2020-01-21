import { Route, Redirect, Switch, Link, useRouteMatch } from "react-router-dom";
import Interval from "./interval";

export default function Summary() {
  const match = useRouteMatch("/summary/interval/:interval");

  return (
    <section id="summary-view">
      <img
        src="/static/apps/mmt-my-money-calendar/img/4.png"
        alt=""
        height="42"
        class="u-hide-on-print"
      />
      <h3>Summary</h3>
      <br />
      <img
        src="/static/apps/mmt-my-money-calendar/img/green_calendar.png"
        alt=""
        width="200"
        class="u-hide-on-print"
      />
      <h3>Here are some totals</h3>
      <p>Check off which expenses you incur.</p>
      <ul>
        <li>Week 1 total?</li>
        <li>Week 2 total?</li>
        <li>Month total?</li>
      </ul>
      <Link to="/">Back Home</Link>
      <br />
      <br />
    </section>
  );
}
