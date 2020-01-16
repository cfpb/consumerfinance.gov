import { Link, useRouteMatch } from "react-router-dom";

export default function Step() {
  const match = useRouteMatch("/interval/:interval");

  return (
    <div className="interval">
      <h2>Interval {match.params.interval}</h2>
    </div>
  );
}
