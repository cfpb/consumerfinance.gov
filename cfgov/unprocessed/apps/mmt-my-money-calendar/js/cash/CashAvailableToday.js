import React from "react";
import { formatCurrency, totalAmount } from "../services/currencyServices";
import { joinClasses } from "../services/stringServices";
import { isEmpty } from "lodash";

export const CashAvailableToday = ({
  incomes,
  expenses,
  startBalance,
  isStyled
}) => {
  const cashAvailable =
    (startBalance || 0) + totalAmount(incomes) - totalAmount(expenses);

  const hasEntries = !isEmpty(incomes) || !isEmpty(expenses);

  const classname =
    isStyled || hasEntries ? (cashAvailable > 0 ? "green" : "red") : "";

  return (
    <div className={joinClasses(["section", "cash-available", classname])}>
      <p className="label">Available cash as of today:</p>
      <p className="value">{formatCurrency(cashAvailable)}</p>
    </div>
  );
};

CashAvailableToday.defaultProps = {
  incomes: [],
  expenses: [],
  startBalance: null,
  isStyles: null
};
