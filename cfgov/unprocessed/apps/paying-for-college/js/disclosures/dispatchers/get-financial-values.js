import financialModel from '../models/financial-model.js';

const getFinancialValues = {
  values: function () {
    return financialModel.values;
  },
};

export default getFinancialValues;
