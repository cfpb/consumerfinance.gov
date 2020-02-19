import clsx from 'clsx';
import { DateTime } from 'luxon';
import { useState, useCallback } from 'react';
import { formatCurrency, toCents } from '../lib/currency-helpers';

export const Checkbox = ({ id, name, onChange, checked, label, value = '1', ...props }) => (
  <div className="m-form-field m-form-field__checkbox">
    <input
      className="a-checkbox"
      type="checkbox"
      name={name}
      id={id}
      onChange={onChange}
      checked={checked}
      value={value}
      {...props}
    />
    <label className="a-label" htmlFor={id}>
      {label}
    </label>
  </div>
);

export const TextField = ({ id, name, type = 'text', onChange, onBlur, label, value, ...props }) => (
  <div className="m-form-field m-form-field__text">
    <label className="a-label a-label__heading" htmlFor={id}>
      {label}
    </label>
    <input type={type} className="a-text-input" id={id} value={value} onChange={onChange} onBlur={onBlur} {...props} />
  </div>
);

export const DateField = ({ onChange, value, ...props }) => (
  <TextField type="date" onChange={onChange} value={value} {...props} />
);

export const CurrencyField = ({ id, name, onChange, onBlur, label, value, ...props }) => {
  // TODO: Consider making this a number field when focused with a pattern of "\d+", which will use a number pad keyboard on mobile

  const handleChange = useCallback(
    (evt) => {
      evt.target.value = toCents(evt.target.value);
      onChange(evt);
    },
    [value, onChange]
  );

  return (
    <TextField
      id={id}
      name={name}
      onChange={handleChange}
      onBlur={onBlur}
      label={label}
      value={formatCurrency(value / 100)}
      {...props}
    />
  );
};

export const RadioButton = ({
  id,
  name,
  onChange,
  label,
  value,
  checked = false,
  largeTarget = false,
  hint,
  ...props
}) => {
  const classes = clsx('m-form-field', 'm-form-field__radio', {
    'm-form-field__lg-target': largeTarget,
  });

  return (
    <div className={classes}>
      <input
        className="a-radio"
        type="radio"
        id={id}
        name={name}
        value={value}
        checked={checked}
        onChange={onChange}
        {...props}
      />
      <label className="a-label" htmlFor={id}>
        {label}
        {hint && <small className="a-label_helper">{hint}</small>}
      </label>
    </div>
  );
};

export const SelectField = ({
  id,
  name,
  label,
  onChange,
  onBlur,
  value,
  placeholder = 'Select an option',
  options = [],
  ...props
}) => {
  const opts = [
    <option value={null} key="empty">
      {placeholder}
    </option>,
    ...options.map(({ label: optLabel, value: optVal }) => (
      <option value={optVal} key={optVal}>
        {optLabel}
      </option>
    )),
  ];

  return (
    <div className="m-form-field m-form-field__select">
      <label className="a-label a-label__heading" htmlFor={id}>
        {label}
      </label>
      <div className="a-select">
        <select id={id} name={name} value={value} onChange={onChange} onBlur={onBlur} {...props}>
          {opts}
        </select>
      </div>
    </div>
  );
};
