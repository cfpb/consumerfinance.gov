import React from "react";

export const CashEditName = ({ config, name, setName }) => (
  <div className="name modal-input">
    <label htmlFor="name">
      <span className="capitalize">{config.type}</span> name
    </label>
    <p className="description">
      Giving your {config.type} a name will help you identify it from other
      similar {config.type}s.
    </p>
    <input
      type="text"
      id="name"
      placeholder={config.namePlaceholder}
      onChange={e => setName(e.target.value)}
      value={name}
    />
  </div>
);

CashEditName.defaultProps = {
  config: {},
  name: "",
  setName: null
};
