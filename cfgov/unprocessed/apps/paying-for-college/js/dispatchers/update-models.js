/**
 * Update the values of models
 */

import { expensesModel } from '../models/expenses-model.js';
import { financialModel } from '../models/financial-model.js';
import { financialView } from '../views/financial-view.js';
import { getSchoolData } from '../dispatchers/get-api-values.js';
import { schoolModel } from '../models/school-model.js';
import { stateModel } from '../models/state-model.js';
import { stringToNum } from '../util/number-utils.js';
import { getConstantsValue, getSchoolValue, getStateValue } from '../dispatchers/get-model-values.js';
import { updateGradMeterChart, updateRepaymentMeterChart, updateSchoolView } from './update-view.js';

const _urlParamsToModelVars = {
  'iped': 'schoolModel.schoolID',
  'pid': 'schoolModel.PID',
  'oid': 'schoolModel.oid',

  'houp': 'stateModel.programHousing',
  'typp': 'stateModel.programType',
  'lenp': 'stateModel.programLength',
  'ratp': 'stateModel.programRate',
  'depp': 'stateModel.programStudentType',
  'cobs': 'stateModel.stateCosts',
  'regs': 'stateModel.stateRegion',
  'iqof': 'stateValues.impactOffer',
  'iqlo': 'stateValues.impactLoans',

  'tuit': 'financialModel.dirCost_tuition',
  'hous': 'financialModel.dirCost_housing',
  'diro': 'financialModel.dirCost_other',

  'book': 'financialModel.indiCost_books',
  'indo': 'financialModel.indiCost_other',
  'nda':  'financialModel.indiCost_added',
  'tran': 'financialValues.indiCost_other',

  'pelg': 'financialModel.grant_pell',
  'seog': 'financialModel.grant_seog',
  'fedg': 'financialModel.grant_federal',
  'stag': 'financialModel.grant_state',
  'schg': 'financialModel.grant_school',
  'othg': 'financialModel.grant_other',

  'mta': 'financialModel.mil_milTuitAssist',
  'gi': 'financialModel.mil_GIBill',
  'othm': 'financialModel.mil_other',

  'stas': 'financialModel.scholarship_state',
  'schs': 'financialModel.scholarship_school',
  'oths': 'financialModel.scholarship_other',

  'wkst': 'financialModel.workStudy_workStudy',

  'fell': 'financialModel.fund_fellowship',
  'asst': 'financialModel.fund_assistantship',

  'subl': 'financialModel.fedLoan_directSub',
  'unsl': 'financialModel.fedLoan_directUnsub',

  'insl': 'financialModel.publicLoan_institutional',
  'insr': 'financialModel.rate_institutional',
  'insf': 'financialModel.fee_institutional',
  'stal': 'financialModel.publicLoan_state',
  'star': 'financialModel.rate_stateLoan',
  'staf': 'financialModel.fee_stateLoan',
  'npol': 'financialModel.publicLoan_nonprofit',
  'npor': 'financialModel.rate_nonprofit',
  'npof': 'financialModel.fee_nonprofit',

  'pers': 'financialModel.savings_personal',
  'fams': 'financialModel.savings_family',
  '529p': 'financialModel.savings_529',

  'offj': 'financialModel.income_jobOffCampus',
  'onj': 'financialModel.income_jobOnCampus',
  'eta': 'financialModel.income_employerAssist',
  'othf': 'financialModel.income_other',

  'pvl1': 'financialModel.privLoan_privLoan1',
  'pvr1': 'financialModel.privloan_privLoanRate1',
  'pvf1': 'financialModel.privloan_privLoanFee1',

  'plus': 'financialModel.fedLoan_parentPlus',

  'houx': 'expensesModel.item_housing',
  'fdx': 'expensesModel.item_food',
  'clhx': 'expensesModel.item_clothing',
  'trnx': 'expensesModel.item_transportation',
  'hltx': 'expensesModel.item_healthcare',
  'entx': 'expensesModel.item_entertainment',
  'retx': 'expensesModel.item_retirement',
  'taxx': 'expensesModel.item_taxes',
  'chcx': 'expensesModel.item_childcare',
  'othx': 'expensesModel.item_other',
  'dbtx': 'expensesModel.item_currentDebt'
};

/**
 * initializeFinancialModel - Create financial model values based on the input
 * fields that exist in the DOM
 */
function initializeFinancialValues() {
  const financialItems = document.querySelectorAll( '[data-financial-item]' );
  financialItems.forEach( elem => {
    financialModel.createFinancialProperty( elem.dataset.financialItem, 0 );
  } );
}

/**
  * updateFinancial - Update a property of the financial model
  * @param {String} name - The name of the property to update
  * @param {*} value - The new value of the property
  * @param {Boolean} updateView - (defaults true) should view be updated?
  */
function updateFinancial( name, value, updateView ) {
  financialModel.setValue( name, value );
}

/**
  * createFinancial - Create a new financial property
  * @param {String} name - The name of the property to update
  * @param {*} value - The new value of the property
  */
function createFinancial( name, value ) {
  financialModel.createFinancialProperty( name, value );
}

/**
  * recalculateFinancials - Run the financialModel's internal calculations
  */
function recalculateFinancials() {
  financialModel.recalculate();
}

/**
  * updateExpense - Update a property of the expense model
  * @param {String} name - The name of the property to update
  * @param {*} value - The new value of the property
  * @param {Boolean} updateView - (defaults true) should view be updated?
  */
function updateExpense( name, value, updateView ) {
  expensesModel.setValue( name, value );
}

/**
  * recalculateExpenses - Run the expenseModel's internal calculations
  */
function recalculateExpenses() {
  expensesModel.calculateTotals();
}

/**
 * updateRegion - Update the region of the expenses model 
 * @param {string} region - A two-character string of the new region
 */
 function updateRegion( region ) {
  expensesModel.setValuesByRegion( region );
 }

/**
  * updateSchoolData - Fetch API data for school and update the model
  * @param {String} iped - The id of the school
  * @returns {Object} Promise of the XHR request
  */
const updateSchoolData = function( iped ) {
  return new Promise( ( resolve, reject ) => {
    getSchoolData( iped )
      .then( resp => {
        const data = JSON.parse( resp.responseText );

        for ( const key in data ) {
          schoolModel.setValue( key, data[key] );
        }

        // Some values must migrate to the financial model
        financialModel.setValue( 'salary_annual', stringToNum( getSchoolValue( 'medianAnnualPay6Yr' ) ) );
        financialModel.setValue( 'salary_monthly', stringToNum( getSchoolValue( 'medianAnnualPay6Yr' ) ) / 12 );

        updateSchoolView();

        resolve( true );

      } )
      .catch( function( error ) {
        reject( error );
        // console.log( 'An error occurred!', error );
      } );
  } );
};

/**
 * updateFinancialsFromSchool - Copies useful values from the schoolModel to the financialModel
 */
const updateFinancialsFromSchool = function() {
  financialModel.updateModelFromSchoolModel();
  financialView.updateFinancialItems();
};

/**
 * updateModelsFromQueryString - Takes an object build from the question string and updates
 * the models with those values
 * @param {Object} queryObj - An object representing the url query string.
 */
function updateModelsFromQueryString( queryObj ) {
  const modelMatch = {
    expensesModel: expensesModel.setValue,
    financialModel: financialModel.setValue,
    schoolModel: schoolModel.setValue,
    stateModel: stateModel.setValue
  };
  for ( const key in queryObj ) {
    if ( _urlParamsToModelVars.hasOwnProperty( key ) ) {
      const match = _urlParamsToModelVars[key].split( '.' );
      modelMatch[match[0]]( match[1], queryObj[key], false );

      // If there's an iped, do a fetch of the schoolData
      if ( key === 'iped' ) {
        updateSchoolData( queryObj[key] );
      }

      // Also put programLength into the financial model
      if ( key === 'lenp' ) {
        financialModel.setValue( 'other_programLength', stringToNum( queryObj[key], false ) );
      }
    }
  }

}

export {
  createFinancial,
  initializeFinancialValues,
  recalculateExpenses,
  recalculateFinancials,
  updateExpense,
  updateFinancial,
  updateFinancialsFromSchool,
  updateModelsFromQueryString,
  updateRegion,
  updateSchoolData,
};
