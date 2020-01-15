import React, { useContext } from "react";

import {
  formatCurrency,
  findPercentage
} from "../../../services/currencyServices";

import {
  savingsTotal,
  expenseTotal
} from "../../../services/cashFlowServices.js";
import { AppContext } from "../../../App";
import { ProgressBar } from "../../shared/ProgressBar";

import "../../../styles/CurrentMonthSummaryChart.scss";

export const CurrentMonthSummaryChart = () => {
  const { monthlyData, selectedMonth } = useContext(AppContext);

  const incomeTotal = Object.keys(monthlyData[selectedMonth.label].incomes)
    .map(key => monthlyData[selectedMonth.label].incomes[key].amount)
    .reduce((total, current) => total + current, 0);

  let expenseObj = Object.keys(monthlyData[selectedMonth.label].expenses)
    .map(key => monthlyData[selectedMonth.label].expenses[key])
    .map(key => ({
      amount: key.amount,
      type: key.type
    }));

  const monthGrandTotal =
    incomeTotal + expenseTotal(expenseObj) + savingsTotal(expenseObj);

  return (
    <div className="current-month-summary-chart-wrapper">
      <ul className="current-month-summary-chart">
        <li>
          <div className="title">Income</div>
          <ProgressBar
            percentage={findPercentage(incomeTotal, monthGrandTotal)}
          />
          <div className="total-value">{formatCurrency(incomeTotal)}</div>
        </li>
        <li>
          <div className="title">Expenses</div>
          <ProgressBar
            percentage={findPercentage(
              expenseTotal(expenseObj),
              monthGrandTotal
            )}
          />
          <div className="total-value">
            {formatCurrency(expenseTotal(expenseObj))}
          </div>
        </li>
        <li>
          <div className="title">Savings</div>
          <ProgressBar
            percentage={findPercentage(
              savingsTotal(expenseObj),
              monthGrandTotal
            )}
          />
          <div className="total-value">
            {formatCurrency(savingsTotal(expenseObj))}
          </div>
        </li>
      </ul>
    </div>
  );
};
