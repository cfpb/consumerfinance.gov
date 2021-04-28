const financialModel = require( '../models/financial-model' );

const getFinancialValues = {
  values: function() {
    return financialModel.values;
  }
};

module.exports = getFinancialValues;
