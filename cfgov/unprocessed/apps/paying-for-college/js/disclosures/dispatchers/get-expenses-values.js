import expensesModel from '../models/expenses-model.js';

const getExpenses = {
  values: function () {
    return expensesModel.values;
  },
};

export default getExpenses;
