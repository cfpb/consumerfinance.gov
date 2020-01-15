import React from "react";
// import Calendar from "../summary/month/Calendar";
// import CashAvailableMonth from "./month/totals/CashAvailableMonth";
// import CurrentMonthSummary from "./month/totals/CurrentMonthSummary";

export const Month = ({ title }) => {
  return (
    <div className="month">
      <div className="page-title">This is the month summary</div>
      <div className="body">
        <div>Month Calendar will go here</div>
        {/* <Calendar /> */}
        <div>Current Month Totals will go here</div>
        {/* <CurrentMonthSummary /> */}
      </div>
      <div>Progress Bar could go here</div>
      {/* <CashAvailableMonth /> */}
    </div>
  );
};
