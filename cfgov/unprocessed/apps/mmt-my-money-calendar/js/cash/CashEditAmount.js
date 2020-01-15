import React from "react";
import { formatCurrency, toCents } from "../services/currencyServices";

export const CashEditAmount = ({ amount, setAmount }) => (
  <div className="amount modal-input">
    <label htmlFor="amount">Amount</label>
    <p className="description">Ex: $1,000.56</p>
    <input
      type="text"
      id="amount"
      onChange={e => setAmount(toCents(e.target.value))}
      value={formatCurrency(amount)}
    />
  </div>
);

CashEditAmount.defaultProps = {
  amount: 0,
  setAmount: null
};
