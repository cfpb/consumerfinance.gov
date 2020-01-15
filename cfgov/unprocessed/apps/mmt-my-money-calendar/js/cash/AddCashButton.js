import React from "react";
import plusIcon from "../../assets/plus-icon.png";

export const AddCashButton = ({
  addButtonText,
  setEditing,
  setSelected,
  date
}) => (
  <div
    className="text-button add-cash"
    onClick={() => handleClick(setEditing, setSelected, date)}
  >
    <span>{addButtonText}</span>
    <img src={plusIcon} alt="circled plus" />
  </div>
);

const handleClick = (setEditing, setSelected, date) => {
  setEditing(true);
  setSelected({
    id: Date.now(),
    type: null,
    name: null,
    amount: null,
    recurring: false,
    date
  });
};

AddCashButton.defaultProps = {
  addButtonText: null,
  setEditing: null,
  setSelected: null,
  date: null
};
