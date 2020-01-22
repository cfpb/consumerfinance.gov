import { Link, useRouteMatch } from "react-router-dom";

export default function StartingBalance() {
  return (
    <div className="starting-balance">
      <img
        src="/static/apps/mmt-my-money-calendar/img/1.png"
        alt=""
        height="42"
        className="u-hide-on-print"
      />
      <h3>Starting Balance</h3>
      <img
        src="/static/apps/mmt-my-money-calendar/img/thinking.png"
        alt=""
        height="100"
        className="u-hide-on-print"
      />
      <h3>Let's figure out your Starting Balance</h3>
      <p>Where do you have money?</p>
      <ul>
        <li>Checking account</li>
        <li>Savings account</li>
        <li>Cash</li>
        <li>Prepaid Cards</li>
        <li>Other</li>
        <li>None</li>
      </ul>
      <br />
      <br />
      <Link to="/wizard/steps/income">Go to Income</Link>
      <br />
      <br />
    </div>
  );
}
