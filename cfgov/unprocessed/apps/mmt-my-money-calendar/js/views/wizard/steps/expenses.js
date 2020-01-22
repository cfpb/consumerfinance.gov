import { Link, useParams } from "react-router-dom";

export default function Expenses() {
  const params = useParams();

  console.log("params: %O", params);
  console.log("params.step: %O", params.step);

  return (
    <div className="expenses">
      <img
        src="/static/apps/mmt-my-money-calendar/img/3a.png"
        alt=""
        height="42"
        className="u-hide-on-print"
      />
      <h3>Income</h3>
      <img
        src="/static/apps/mmt-my-money-calendar/img/thinking.png"
        alt=""
        height="100"
        className="u-hide-on-print"
      />
      <h3>What expenses do you have?</h3>
      <p>Check off which expenses you incur.</p>
      <ul>
        <li>Electricity</li>
        <li>Gas</li>
        <li>Phone</li>
        <li>Internet</li>
        <li>Other</li>
      </ul>
      <br />
      <br />
      <Link to="/summary">Go to Summary</Link>
      <br />
      <br />
    </div>
  );
}
