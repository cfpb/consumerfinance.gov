import expensesModel from '../models/expenses-model.js';

const getExpensesValues = {
  values: function () {
    return expensesModel.values;
  },
};

export default getExpensesValues;
