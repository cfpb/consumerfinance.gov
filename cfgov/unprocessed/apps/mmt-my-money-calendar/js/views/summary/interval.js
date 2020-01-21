import { Link, useRouteMatch } from "react-router-dom";

export default function Interval() {
  // Interval will be either month or week
  const match = useRouteMatch("/interval/:interval");

  return (
    <div className="interval">
      <img
        src="/static/apps/mmt-my-money-calendar/img/4.png"
        alt=""
        height="42"
        class="u-hide-on-print"
      />
      <h3>Summary</h3>
      <img
        src="/static/apps/mmt-my-money-calendar/img/green_calendar.png"
        alt=""
        height="100"
        class="u-hide-on-print"
      />
      <h3>Here are some totals</h3>
      <p>Check off which expenses you incur.</p>
      <ul>
        <li>Electricity</li>
        <li>Gas</li>
        <li>Phone</li>
        <li>Internet</li>
        <li>Other</li>
      </ul>
      <h2>Interval {match.params.interval}</h2>
    </div>
  );
}
