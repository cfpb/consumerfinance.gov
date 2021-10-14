// This file contains the model for after-college expenses
import {
  updateAffordingChart,
  updateCostOfBorrowingChart,
  updateExpensesView,
  updateUrlQueryString } from '../dispatchers/update-view.js';
import { getExpenses } from '../dispatchers/get-api-values.js';
import { getFinancialValue } from '../dispatchers/get-model-values.js';
import { stringToNum } from '../util/number-utils.js';
import { updateState } from '../dispatchers/update-state.js';

// Please excuse some uses of underscore for code/HTML property clarity!
/* eslint camelcase: ["error", {properties: "never"}] */

const expensesModel = {
  // Values of the currently selected region
  values: {
    item_clothing: 0,
    item_entertainment: 0,
    item_food: 0,
    item_healthcare: 0,
    item_housing: 0,
    item_retirement: 0,
    item_taxes: 0,
    item_transportation: 0,
    item_othe: 0,
    item_childcare: 0,
    item_currentDebts: 0
  },

  // All data from the API
  rawData: {},

  /**
   * Calculate total monthly expenses
   */
  calculateTotals: () => {
    let totalExpenses = 0;
    const remaining = 0;

    for ( const prop in expensesModel.values ) {
      if ( prop.substring( 0, 5 ) === 'item_' ) {
        totalExpenses += expensesModel.values[prop];
      }
    }

    expensesModel.values.total_expenses = totalExpenses;
    expensesModel.values.total_remainder = getFinancialValue( 'salary_monthly' ) - totalExpenses -
      getFinancialValue( 'debt_tenYearMonthly' );
    if ( expensesModel.values.total_remainder > 0 ) {
      updateState.byProperty( 'expensesRemainder', 'surplus' );
    } else if ( expensesModel.values.total_remainder < 0 ) {
      updateState.byProperty( 'expensesRemainder', 'shortage' );
    }

    updateExpensesView();

  },

  /**
   * setValue - Used to set a value
   * @param {String} name - Property name
   * @param {Number} value - New value of property
   * @param {Boolean} updateView - (defaults true) should view be updated?
   */
  setValue: ( name, value, updateView ) => {
    expensesModel.values[name] = stringToNum( value );
    expensesModel.calculateTotals();
    if ( updateView !== false ) {
      updateExpensesView();
    }
  },

  /**
   * Turns a salary number into a salary range for use in retrieving
   * the correct BLS expense values.
   * @param {number} salary - Number value of salary
   * @returns {string} salaryRange - String representing salary range
   */
  _getSalaryRange: function( salary ) {
    const rangeFinder = {
      'less_than_5000': [ 0, 4999 ],
      '5000_to_9999':   [ 5000, 9999 ],
      '10000_to_14999': [ 10000, 14999 ],
      '15000_to_19999': [ 15000, 19999 ],
      '20000_to_29999': [ 20000, 29999 ],
      '30000_to_39999': [ 30000, 39999 ],
      '40000_to_49999': [ 40000, 49999 ],
      '50000_to_69999': [ 50000, 69999 ],
      '70000_or_more':  [ 70000, Infinity ]
    };

    let arr;
    for ( const key in rangeFinder ) {
      if ( rangeFinder.hasOwnProperty( key ) ) {
        arr = rangeFinder[key];
        if ( salary >= arr[0] && salary <= arr[1] ) {
          return key;
        }
      }
    }

    return 'salary not found';
  },

  /**
   * Change values based on region, using data stored in rawData property
   * @param {string} region - Two letter code for region
   */
  setValuesByRegion( region ) {
    const propertyTranslator = {
      Clothing: 'item_clothing',
      Entertainment: 'item_entertainment',
      Food: 'item_food',
      Healthcare: 'item_healthcare',
      Housing: 'item_housing',
      Retirement: 'item_retirement',
      Taxes: 'item_taxes',
      Transportation: 'item_transportation',
      Other: 'item_other'
    };

    const salary = getFinancialValue( 'salary_annual' ) || 0;
    const salaryRange = expensesModel._getSalaryRange( salary );

    for ( const key in propertyTranslator ) {
      if ( propertyTranslator.hasOwnProperty( key ) ) {
        const data = expensesModel.rawData[key];
        if ( data ) {
          let value = stringToNum(
            expensesModel.rawData[key][region][salaryRange]
          );
          value = Math.round( value / 12 );
          expensesModel.values[propertyTranslator[key]] = value;
        }
      }
    }

    expensesModel.calculateTotals();
    updateUrlQueryString();
  },

  /**
   * Initialize the model, fetch values from API
   * @returns {Promise} The promised init response
   */
  init: function() {
    return new Promise( ( resolve, reject ) => {
      getExpenses()
        .then( resp => {
          expensesModel.rawData = JSON.parse( resp.responseText );
          updateExpensesView();
          resolve( true );
        } )
        .catch( function( error ) {
          reject( error );
          console.log( 'An error occurred when accessing the expenses API', error );
        } );
    } );
  }
};

export {
  expensesModel
};
