import { useEffect } from "react";
import { Link, useRouteMatch } from "react-router-dom";

export default function Step() {
  const match = useRouteMatch("/wizard/step/:step");

  console.log("match inside step is: ", match);
  console.log("match.params", match.params);
  console.log("match.params.step", match.params.step);
  //testing console.log

  return (
    <div className="wizard-step">
      <h2>Step {match.params.step}</h2>
    </div>
  );
}
