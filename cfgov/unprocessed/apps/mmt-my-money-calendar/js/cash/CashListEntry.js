import React from "react";
import { formatCurrency } from "../services/currencyServices";

const handleEdit = ({ current, setEditing, setSelected }) => {
  setSelected(current);
  setEditing(true);
};

export const CashListEntry = props => {
  const { name, amount } = props.current;
  const sign = props.section === "expenses" ? "- " : "";

  return (
    <div className="entry">
      <div className="row">
        <p className="name">{name}</p>
        <div className="text-button" onClick={() => handleEdit(props)}>
          <span>edit</span>
        </div>
      </div>
      <p className="amount">
        {sign}
        {formatCurrency(amount)}
      </p>
    </div>
  );
};

CashListEntry.defaultProps = {
  current: {},
  setEditing: null,
  setSelected: null
};
