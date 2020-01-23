import clsx from 'clsx';

export const Checkbox = ({ id, name, onChange, checked, label, value = '1', ...props }) => (
  <div className="m-form-field m-form-field__checkbox">
    <input className="a-checkbox" type="checkbox" name={name} id={id} onChange={onChange} checked={checked} value={value} />
    <label className="a-label" htmlFor={id}>{label}</label>
  </div>
);
