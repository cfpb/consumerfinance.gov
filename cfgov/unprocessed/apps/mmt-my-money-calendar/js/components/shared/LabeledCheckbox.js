import React from "react";
// import "../../styles/LabeledCheckbox.scss";
import { joinClasses } from "../../stringServices";

export const LabeledCheckbox = ({
  checked,
  id,
  update,
  name,
  label,
  cname = ""
}) => (
  <label className={joinClasses(["checkbox-container", cname])} htmlFor={id}>
    {label}
    <input
      id={id}
      name={name}
      type="checkbox"
      checked={checked}
      onChange={e => update(e.target.checked)}
    />
    <span className="checkmark"></span>
  </label>
);
