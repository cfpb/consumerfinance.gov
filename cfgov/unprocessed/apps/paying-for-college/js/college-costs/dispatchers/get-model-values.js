/**
 * Update the values of models
 */

import { constantsModel } from '../models/constants-model.js';
import { expensesModel } from '../models/expenses-model.js';
import { financialModel } from '../models/financial-model.js';
import { schoolModel } from '../models/school-model.js';
import { stateModel } from '../models/state-model.js';


/**
 * getAllStateValues - retrieves the entire values property (object) of the stateModel
 * @returns {Object} The values stored in the stateModel Object
 */
function getAllStateValues() {
  return { ...stateModel.values };
}

/**
 * getConstantsValue - get the value of 'name' from the constantsModel
 * @param {string} name - Name of the property to retrieve
 * @returns {(number|string|boolean)} value of the property, false if undefined
 */
function getConstantsValue( name ) {
  if ( constantsModel.values.hasOwnProperty( name ) ) {
    return constantsModel.values[name];
  }
  return false;

}

/** 3
 * getExpensesValue - get the value of 'name' from the expensesModel
 * @param {string} name - Name of the property to retrieve
 * @returns {number} value of the property
 */
function getExpensesValue( name ) {
  return expensesModel.values[name];
}

/**
 * getFinancialValue - get the value of 'name' from the financialModel
 * @param {string} name - Name of the property to retrieve
 * @returns {number|booleab} value of the property, or false if undefined
 */
function getFinancialValue( name ) {
  if ( financialModel.values.hasOwnProperty( name ) ) {
    return financialModel.values[name];
  }
  return false;

}

/**
 * getProgramList - retrieve an alphabetical list of programs
 * from the schoolModel
 * @param {string} level - program level - 'undergrad' or 'graduate'
 * @returns {array} an arry of objects containing program data
 */
function getProgramList( level ) {
  return schoolModel.getAlphabeticalProgramList( level );
}

/**
 * getProgramInfo - retrieve info based on pid
 * @param {string} pid - Program ID
 * @returns {object} Values of the program
 */
function getProgramInfo( pid ) {
  return schoolModel.getProgramInfo( pid );
}

/**
 * Retrieves the cohort values for meter graphs
 * @param {string} cohort - The cohort property to search
 * @param {string} property - The property inside the cohort data to retrieve
 * @returns {object} An object with the data for the cohort and property
 */
function getSchoolCohortValue( cohort, property ) {
  const smv = schoolModel.values;
  if ( smv.hasOwnProperty( cohort ) && smv[cohort].hasOwnProperty( property ) ) {
    return smv[cohort][property];
  }
  return { percentile_rank: 0, error: 'no property found' };
}

/**
 * getSchoolValue - get the value of 'name' from the schoolModel
 * @param {string} name - Name of the property to retrieve
 * @returns {(number|string|boolean)} value of the property, or false if undefined
 */
function getSchoolValue( name ) {
  if ( schoolModel.values.hasOwnProperty( name ) ) {
    return schoolModel.values[name];
  }
  return false;
}

/**
 * getStateValue - gets the property from the application state model
 * @param {string} prop - The property name
 * @returns {stringboolean} The value of the property in the stateModel Object, or
 *    false if undefined
 */
function getStateValue( prop ) {
  if ( stateModel.values.hasOwnProperty( prop ) ) {
    return stateModel.values[prop];
  }
  return false;

}

export {
  getAllStateValues,
  getConstantsValue,
  getExpensesValue,
  getFinancialValue,
  getProgramInfo,
  getProgramList,
  getSchoolCohortValue,
  getSchoolValue,
  getStateValue
};
