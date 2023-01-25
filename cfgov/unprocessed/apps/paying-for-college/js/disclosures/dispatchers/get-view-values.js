import { convertStringToNumber } from '../../../../../js/modules/util/format.js';

const getViewValues = {
  def: 0,

  init: function (apiValues) {
    return Object.assign(this.inputs(), apiValues);
  },

  getPrivateLoans: function (values) {
    // Note: Only run once, during init()
    const privateLoans = document.querySelectorAll('[data-private-loan]');
    values.privateLoanMulti = [];
    privateLoans.forEach((ele) => {
      const fields = ele.querySelectorAll('[data-private-loan_key]');
      const loanObject = { amount: 0, totalLoan: 0, rate: 0, deferPeriod: 0 };
      fields.forEach((field) => {
        const key = field.getAttribute('data-private-loan_key');
        let value = field.value;
        if (key === 'rate') {
          value /= 100;
        }
        loanObject[key] = convertStringToNumber(value);
      });
      values.privateLoanMulti.push(loanObject);
    });
    return values;
  },

  inputs: function () {
    // Note: Only run once, during init()
    let values = {};
    const elements = document.querySelectorAll('[data-financial]');

    elements.forEach((elem) => {
      if (!elem.hasAttribute('data-private-loan_key')) {
        const name = elem.getAttribute('data-financial');
        values[name] = convertStringToNumber(elem.value) || 0;
        if (elem.getAttribute('data-percentage_value') === 'true') {
          values[name] /= 100;
        }
      }
    });

    values = this.getPrivateLoans(values);

    return values;
  },
};

export default getViewValues;
