import { useEffect } from "react";
import { Link, useRouteMatch } from "react-router-dom";

export default function Income() {
  const match = useRouteMatch("/wizard/steps/:step");

  console.log("match inside step is: ", match);
  console.log("match.params", match.params);
  console.log("match.params.step", match.params.step);
  //testing console.log

  return (
    <div className="income">
      <img
        src="/static/apps/mmt-my-money-calendar/img/2.png"
        alt=""
        height="42"
        class="u-hide-on-print"
      />
      <h3>Income</h3>
      <img
        src="/static/apps/mmt-my-money-calendar/img/thinking.png"
        alt=""
        height="100"
        class="u-hide-on-print"
      />
      <h3>Tell us about your income</h3>
      <p>Check off which types of income you receive.</p>
      <ul>
        <li>Job</li>
        <li>Child Support</li>
        <li>TANF</li>
        <li>Veterans Benefits</li>
        <li>Social Security</li>
        <li>Other</li>
      </ul>
      <br />
      <br />
      <Link to="/wizard/steps/expenses">Go to Expenses</Link>
      <br />
      <br />
    </div>
  );
}
