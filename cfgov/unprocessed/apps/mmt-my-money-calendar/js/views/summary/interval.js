import { Link, useRouteMatch } from "react-router-dom";

export default function Interval() {
  // Interval will be either month or week
  const match = useRouteMatch("/interval/:interval");

  return (
    <div className="interval">
      <div>missy interval</div>
      <h2>Interval {match.params.interval}</h2>
    </div>
  );
}
