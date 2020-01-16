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
      <h2>Step {match.params.step}</h2>
      <Link to="/wizard/steps/expenses">Go to Expenses</Link>
    </div>
  );
}
