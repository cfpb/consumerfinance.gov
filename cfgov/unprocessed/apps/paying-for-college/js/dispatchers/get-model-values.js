/**
 * Update the values of models
 */

import { constantsModel } from '../models/constants-model.js';
import { expensesModel } from '../models/expenses-model.js';
import { financialModel } from '../models/financial-model.js';
import { schoolModel } from '../models/school-model.js';
import { stateModel } from '../models/state-model.js';

/**
 * getFinancialValue - get the value of 'name' from the financialModel
 * @param {string} name - Name of the property to retrieve
 * @returns {number} value of the property
 */
function getFinancialValue( name ) {
  return financialModel.values[name];
}

/**
 * getSchoolValue - get the value of 'name' from the schoolModel
 * @param {string} name - Name of the property to retrieve
 * @returns {(number|string)} value of the property
 */
function getSchoolValue( name ) {
  return schoolModel.values[name];
}

/**
 * getExpensesValue - get the value of 'name' from the expensesModel
 * @param {string} name - Name of the property to retrieve
 * @returns {number} value of the property
 */
function getExpensesValue( name ) {
  return expensesModel.values[name];
}

/**
 * getConstantsValue - get the value of 'name' from the constantsModel
 * @param {string} name - Name of the property to retrieve
 * @returns {(number|string)} value of the property
 */
function getConstantsValue( name ) {
  return constantsModel.values[name];
}

/**
 * getStateValue - gets the property from the application state model
 * @param {string} prop - The property name
 * @returns {string} The value of the property in the stateModel Object
 */
function getStateValue( prop ) {
  return stateModel.values[prop];
}

/**
 * getAllStateValues - retrieves the entire values property (object) of the stateModel
 * @returns {Object} The values stored in the stateModel Object
 */
function getAllStateValues( prop ) {
  return Object.assign( {}, stateModel.values );
}


export {
  getFinancialValue,
  getSchoolValue,
  getConstantsValue,
  getExpensesValue,
  getAllStateValues,
  getStateValue
};
