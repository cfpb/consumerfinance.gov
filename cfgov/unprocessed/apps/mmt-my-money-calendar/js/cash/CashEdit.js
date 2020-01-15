import React, { useState } from "react";
import { cashConfig } from "../../config/cashConfig";
import { CashEditAmount } from "./CashEditAmount";
import { CashEditName } from "./CashEditName";
import { CashEditType } from "./CashEditType";
import { LabeledCheckbox } from "../shared/LabeledCheckbox";

export const CashEdit = ({ current, section, setEditing, setState, data }) => {
  const [type, setType] = useState(current.type);
  const [name, setName] = useState(current.name || "");
  const [amount, setAmount] = useState(current.amount || "");
  const [recurring, setRecurring] = useState(current.recurring || false);

  const config = cashConfig[section];

  // Save entry to local state
  const saveEntry = e => {
    e.preventDefault();
    const thisId = current.id || Date.now();

    setEditing(false);
    setState([
      ...data.filter(item => item.id !== thisId),
      {
        id: thisId,
        date: current.date,
        type,
        name,
        amount,
        recurring
      }
    ]);
  };

  // Delete entry from local state
  const deleteEntry = e => {
    e.preventDefault();
    data = data.filter(entry => entry.id !== current.id);
    setEditing(false);
    setState([...data]);
  };

  return (
    <form className="cash-edit" onSubmit={saveEntry}>
      <CashEditType type={type} setType={setType} config={config} />

      {type && <CashEditName name={name} setName={setName} config={config} />}
      {type && <CashEditAmount amount={amount} setAmount={setAmount} />}
      {type && (
        <LabeledCheckbox
          id="recurring"
          checked={recurring}
          update={setRecurring}
          label={`Recurring ${config.type}`}
          cname="modal-input"
        />
      )}

      {type && (
        <div className="form-actions">
          <button className="primary" type="submit" onClick={saveEntry}>
            Save this {config.type}
          </button>
          <button className="secondary" onClick={deleteEntry}>
            Delete this {config.type}
          </button>
        </div>
      )}
    </form>
  );
};

CashEdit.defaultProps = {
  section: "incomes",
  current: {},
  setEditing: null,
  setState: null,
  data: []
};
