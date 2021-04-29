const expensesModel = require( '../models/expenses-model' );

const getExpensesValues = {
  values: function() {
    return expensesModel.values;
  }
};

module.exports = getExpensesValues;
