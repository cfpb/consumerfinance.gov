import React from "react";
import closeIcon from "../../assets/close-icon.png";

export const CashHeader = ({ icon, title, editing, setEditing }) => (
  <div className="cash-header">
    <div className="cash-title">
      <img src={icon} alt="cash flow arrow" />
      <span>{title}</span>
    </div>
    {editing && (
      <div className="text-button" onClick={() => setEditing(false)}>
        <span>Cancel</span>
        <img src={closeIcon} alt="circled x" />
      </div>
    )}
  </div>
);

CashHeader.defaultProps = {
  icon: "",
  title: "",
  editing: false,
  setEditing: null
};
