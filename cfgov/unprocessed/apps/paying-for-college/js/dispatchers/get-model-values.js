/**
 * Update the values of models
 */

import { expensesModel } from '../models/expenses-model.js';
import { financialModel } from '../models/financial-model.js';
import { schoolModel } from '../models/school-model.js';
import { constantsModel } from '../models/constants-model.js';
import { stateModel } from '../models/state-model.js';

const getFinancialValue = function( name ) {
  return financialModel.values[name];
};

const getSchoolValue = function( name ) {
  return schoolModel.values[name];
};

const getExpensesValue = function( name ) {
  return expensesModel.values[name];
};

const getConstantsValue = function( name ) {
  return constantsModel.values[name];
};

/**
 * getStateValue - gets the property from the application state model
 *
 * @param {string} prop - The property name
 *
 * @returns {string} The value of the property in the stateModel Object
 */
const getStateValue = function( prop ) {
  return stateModel.values[prop];
};


export {
  getFinancialValue,
  getSchoolValue,
  getConstantsValue,
  getExpensesValue,
  getStateValue
};
