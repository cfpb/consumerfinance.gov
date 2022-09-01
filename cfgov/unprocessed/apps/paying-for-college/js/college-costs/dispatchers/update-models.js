/**
 * Update the values of models
 */
import { expensesModel } from '../models/expenses-model.js';
import { expensesView } from '../views/expenses-view.js';
import { financialModel } from '../models/financial-model.js';
import { financialView } from '../views/financial-view.js';
import { getStateByCode } from '../util/other-utils.js';
import { getSchoolData } from '../dispatchers/get-api-values.js';
import { schoolModel } from '../models/school-model.js';
import { stateModel } from '../models/state-model.js';
import { isNumeric, stringToNum } from '../util/number-utils.js';
import {
  getProgramInfo,
  getSchoolValue,
  getStateValue
} from '../dispatchers/get-model-values.js';
import { updateSchoolView, updateExpensesView } from './update-view.js';
// import { updateState } from '../dispatchers/update-state.js';
import { urlParameters } from '../util/url-parameter-utils.js';

/**
 * initializeExpenseValues - Create financial model values based on the input
 * fields that exist in the DOM
 */
function initializeExpenseValues() {
  const expenseItems = document.querySelectorAll( '[data-expenses-item]' );
  expenseItems.forEach( elem => {
    expensesModel.setValue( elem.dataset.expensesItem, 0, false );
  } );
}

/**
 * initializeFinancialValues - Create financial model values based on the input
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
  financialModel.setValue( name, value, updateView );
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
 * refreshExpenses - Update the expenses with stored values
 */
function refreshExpenses() {
  expensesModel.setValuesByRegion( schoolModel.values.region );
}

/**
 *
 */
function clearFinancialCosts() {
  financialModel.clearCosts();
}

/**
 * getTopThreePrograms - Update the expenses with stored values
 * @param {String} programs - list of top programs (programsPopular)
 * @returns {String} - top three programs
 */
function getTopThreePrograms( programs ) {
  const topThree = '';
  if ( programs !== null ) {
    const topThreeArr = programs.slice( 0, 3 );
    schoolModel.values.programsTopThree = topThreeArr.join( ', ' );
  }
  return topThree;
}

/**
  * @param {Object} data - Data from school API
  */
function setSchoolValues( data ) {
  for ( const key in data ) {
    const val = data[key];
    schoolModel.setValue( key, val, false );

    // Update state to reflect any missing rate values
    if ( [ 'repay3yr', 'gradRate', 'defaultRate' ].indexOf( key ) > -1 && !isNumeric( val ) ) {
      stateModel.setValue( key + 'missing', true );
    }
  }
}

/**
  * updateSchoolData - Fetch API data for school and update the model
  * @param {String} iped - The id of the school
  * @returns {Object} Promise of the XHR request
  */
function updateSchoolData( iped ) {
  stateModel.setValue( 'schoolID', iped );
  return new Promise( ( resolve, reject ) => {
    getSchoolData( iped )
      .then( resp => {
        const data = JSON.parse( resp.responseText );
        setSchoolValues( data );
        const pid = getStateValue( 'pid' );

        // Create objects of programs keyed by program ID
        schoolModel.createProgramLists();
        const programInfo = getProgramInfo( pid );

        // If we have a pid, validate it has info
        if ( !programInfo ) {
          stateModel.setValue( 'pid', false );
        }

        // Take only the top 3 programs
        schoolModel.values.programsTopThree =
          getTopThreePrograms( schoolModel.values.programsPopular );

        // add the full state name to the schoolModel
        schoolModel.values.stateName =
          getStateByCode( schoolModel.values.state );

        // Some values must migrate to the financial model
        if ( programInfo ) {
          financialModel.setValue( 'salary_annual', stringToNum( programInfo.salary ) );
          stateModel.setValue( 'programName', programInfo.name );
        } else {
          financialModel.setValue( 'salary_annual', stringToNum( getSchoolValue( 'medianAnnualPay6Yr' ) ) );
        }

        // Update expenses by region
        if ( schoolModel.values.hasOwnProperty( 'region' ) ) {
          document.querySelector( '#expenses__region' ).value = schoolModel.values.region;
          updateRegion( schoolModel.values.region );
        }

        updateSchoolView();

        resolve( true );

      } )
      .catch( function( error ) {
        reject( error );
        iped = iped.replace( /\D/g, '' );
        console.log( 'An error occurred when accessing school data for ' + iped, error );
      } );
  } );
}

/**
 * updateFinancialsFromSchool - Copies useful values from the schoolModel to the financialModel
 */
function updateFinancialsFromSchool() {
  financialModel.updateModelFromSchoolModel();
  financialView.updateFinancialItems();
}

/**
 * parseQueryParameters - put query values into models
 * @param {Object} queryObj - an Object containing query key/value pairs
 */
function parseQueryParameters( queryObj ) {
  const modelMatch = {
    expensesModel: expensesModel.setValue,
    financialModel: financialModel.setValue,
    schoolModel: schoolModel.setValue,
    stateModel: stateModel.setValue
  };

  for ( const key in queryObj ) {
    if ( urlParameters.hasOwnProperty( key ) ) {
      const match = urlParameters[key].split( '.' );
      modelMatch[match[0]]( match[1], queryObj[key], false );

      // plus can mean either type of loan (they are mutually exclusive)
      if ( key === 'plus' ) {
        financialModel.setValue( 'plusLoan_gradPlus', stringToNum( queryObj[key] ), false );
      }
    }
  }

  // Copy programLength into the financial model
  financialModel.setValue( 'other_programLength', stringToNum( queryObj.lenp ), false );
}

/**
 * updateModelsFromQueryString - Translate query values into model values
 * @param {Object} queryObj - An object representing the url query string.
 */
function updateModelsFromQueryString( queryObj ) {
  const modelMatch = {
    expensesModel: expensesModel.setValue,
    financialModel: financialModel.setValue,
    schoolModel: schoolModel.setValue,
    stateModel: stateModel.setValue
  };

  // If there's an offerID, set cobs to 'o' (offer)
  if ( queryObj.hasOwnProperty( 'oid' ) ) {
    queryObj.cobs = 'o';
  }

  // If we have no cobs, check if there are costs values
  if ( !queryObj.hasOwnProperty( 'cobs' ) ) {
    const costKeys = [ 'tuit', 'hous', 'diro', 'book', 'indo', 'nda', 'tran' ];
    let costsFound = false;
    costKeys.forEach( key => {
      if ( queryObj.hasOwnProperty( key ) ) {
        costsFound = true;
      }
    } );

    if ( costsFound ) {
      queryObj.cobs = 'y';
    }
  }

  parseQueryParameters( queryObj );
  if ( queryObj.hasOwnProperty( 'iped' ) ) {
    updateSchoolData( queryObj.iped )
      .then( () => {
        updateExpensesFromQueryObj( queryObj );
      } );
  }
}

/**
 * updateExpensesFromQueryObj - Update expenses with queryObj values
 * @param {Object} queryObj - An object representing the url query string.
 */
function updateExpensesFromQueryObj( queryObj ) {
  const params = [ 'houx', 'fdx', 'clhx', 'trnx', 'hltx', 'entx', 'retx',
    'taxx', 'chcx', 'othx' ];
  params.forEach( key => {
    if ( urlParameters.hasOwnProperty( key ) ) {
      const prop = urlParameters[key].split( '.' )[1];
      expensesModel.setValue( prop, queryObj[key], false );
    }
  } );
  expensesView.updateExpensesView();
}

export {
  clearFinancialCosts,
  createFinancial,
  initializeExpenseValues,
  initializeFinancialValues,
  recalculateExpenses,
  recalculateFinancials,
  refreshExpenses,
  updateExpense,
  updateFinancial,
  updateFinancialsFromSchool,
  updateModelsFromQueryString,
  updateRegion,
  updateSchoolData
};
