import React, { useContext } from "react";

import { formatCurrency } from "../../../services/currencyServices";
import { AppContext } from "../../../App";

const CashAvailableMonth = () => {
  const { monthlyData, selectedMonth } = useContext(AppContext);

  const incomeTotal = Object.keys(monthlyData[selectedMonth.label].incomes)
    .map(key => monthlyData[selectedMonth.label].incomes[key].amount)
    .reduce((total, current) => total + current, 0);

  const expenseObj = Object.keys(monthlyData[selectedMonth.label].expenses)
    .map(key => monthlyData[selectedMonth.label].expenses[key])
    .map(key => ({
      amount: key.amount,
      type: key.type
    }));

  const expenseTotal = expenseObj
    .filter(item => item.type.value !== "savings")
    .map(entry => entry.amount)
    .reduce((total, current) => total + current, 0);

  let grandTotal = incomeTotal - expenseTotal;
  let divStyle;
  if (grandTotal >= 0) {
    divStyle = {
      color: "green"
    };
  } else {
    divStyle = {
      color: "red"
    };
  }

  return (
    <div className="cash-available-month-wrapper">
      <div className="page-subtotal">Total Available Cash</div>

      <div style={divStyle}>{formatCurrency(grandTotal)}</div>
    </div>
  );
};

export default CashAvailableMonth;
