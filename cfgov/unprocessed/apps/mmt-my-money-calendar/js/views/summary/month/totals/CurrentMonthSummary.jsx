import React, { useState } from "react";

import "../../../styles/CurrentMonthSummary.scss";

import { CurrentMonthSummaryChart } from "../CurrentMonthSummary/CurrentMonthSummaryChart";
import { ActionLink } from "../../shared/ActionLink";

function CurrentMonthSummary() {
  const [chartvisible, setChartVisible] = useState(false);

  const changeChart = () => {
    setChartVisible(!chartvisible);
  };

  return (
    <div className="current-month-summary-wrapper">
      <div className="monthly-totals-header">
        <div className="page-subtitle">Monthly Totals</div>
        <div className="show-link" onClick={changeChart}>
          {chartvisible ? (
            <ActionLink text="Hide" icon="close-icon" />
          ) : (
            <ActionLink text="Show" icon="open-icon" />
          )}
        </div>
      </div>
      <p className="description">
        Review your total income, expenses and the amount you set aside for
        savings.
      </p>
      {chartvisible ? <CurrentMonthSummaryChart /> : null}
    </div>
  );
}

export default CurrentMonthSummary;
