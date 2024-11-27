import React from 'react';
import { createRoot } from 'react-dom/client';
import Select from 'react-select';

function onChange(val) {
  window.location = `/credit-cards/agreements/issuer/${val.value}/`;
}

function getOption(options, val) {
  for (let i = 0; i < options.length; i++) {
    if (options[i].value === val) return options[i];
  }
  return null;
}

function Wrapper() {
  const options = window.ISSUERS || []
  const defaultValue = document.getElementById('issuer-slug')?.textContent;

  return (
    <Select
      options={options}
      defaultValue={defaultValue ? getOption(options, defaultValue) : null}
      placeholder="Search for an issuer"
      onChange={onChange}
      isSearchable={true}
    />
  );
}

const root = createRoot(document.getElementById('select-root'));
root.render(<Wrapper />);
