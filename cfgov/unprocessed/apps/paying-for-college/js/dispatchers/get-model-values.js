/**
 * Update the values of models
 */

import { expensesModel } from '../models/expenses-model.js';
import { financialModel } from '../models/financial-model.js';
import { schoolModel } from '../models/school-model.js';
import { constantsModel } from '../models/constants-model.js';

const getFinancialValue = function( name ) {
  return financialModel.values[name];
};

const getSchoolValue = function( name ) {
  return schoolModel.values[name];
};

const getConstantsValue = function( name ) {
  return constantsModel.values[name];
};

export {
  getFinancialValue,
  getSchoolValue,
  getConstantsValue
};
