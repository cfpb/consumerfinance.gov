import React from "react";
import Select from "react-select";

export const CashEditType = ({ config, type, setType }) => (
  <div className="type modal-input">
    <label htmlFor="type">
      <span className="capitalize">{config.type}</span> type
    </label>
    <Select
      value={type}
      onChange={setType}
      placeholder={`Select ${config.type} type`}
      options={config.typeOptions}
    />
  </div>
);

CashEditType.defaultProps = {
  config: {},
  type: "",
  setType: null
};
