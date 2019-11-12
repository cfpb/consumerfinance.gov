/**
 * Update the values of models
 */

import { expensesModel } from '../models/expenses-model.js';
import { financialModel } from '../models/financial-model.js';
import { schoolModel } from '../models/school-model.js';

const getFinancialValue = function( name ) {
    return financialModel.values[name];
}

export {
    getFinancialValue
}