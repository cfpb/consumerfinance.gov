import { useEffect } from "react";
import { Link, useRouteMatch } from "react-router-dom";

export default function Expenses() {
  const match = useRouteMatch("/wizard/steps/:step");

  console.log("match  is: ", match);
  console.log("match.params", match.params);
  console.log("match.params.step", match.params.step);
  //testing console.log

  return (
    <div className="expenses">
      <h2>Expenses {match.params.step}</h2>
      <Link to="/summary">Go to Summary</Link>
    </div>
  );
}
