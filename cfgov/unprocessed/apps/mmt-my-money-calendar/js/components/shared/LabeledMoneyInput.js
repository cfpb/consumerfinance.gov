import React from "react";
import { formatCurrency, toCents } from "../../services/currencyServices";

export const LabeledMoneyInput = ({
  type,
  id,
  desc,
  amount,
  setAmount,
  focustarget
}) => (
  <div className="modal-input">
    <div className="label">{type}</div>
    <div className="description">{desc}</div>

    <input
      type="text"
      id={id}
      ref={focustarget}
      onChange={e => setAmount(toCents(e.target.value))}
      value={formatCurrency(amount)}
    />
  </div>
);
