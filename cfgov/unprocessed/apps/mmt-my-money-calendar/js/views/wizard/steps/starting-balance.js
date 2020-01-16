import { Link, useRouteMatch } from "react-router-dom";

export default function StartingBalance() {
  return (
    <div className="starting-balance">
      <h2>Starting Balance Goes Here</h2>
      <Link to="/wizard/steps/income">Go to Income</Link>
    </div>
  );
}
