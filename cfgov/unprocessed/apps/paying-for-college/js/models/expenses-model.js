// This file contains the model for after-college expenses
import { financialModel } from './financial-model.js';
import { getExpenses } from '../dispatchers/get-api-values.js';
import { getFinancialValue } from '../dispatchers/get-model-values.js';
import { stringToNum } from '../util/number-utils.js';
import { updateExpensesView, updateFinancialView } from '../dispatchers/update-view.js';

const expensesModel = {
  // Values of the currently selected region
  values: {},

  // All data from the API
  rawData: {},


  /**
   * Calculate total monthly expenses
   */
  calculateTotals: () => {
    let totalExpenses = 0;
    let remaining = 0;

    for ( const prop in expensesModel.values ) {
      if ( prop.substring( 0, 5 ) === 'item_' ) {
        totalExpenses += expensesModel.values[prop];
      }
    }

    expensesModel.values.total_expenses = totalExpenses;
    expensesModel.values.total_remainder = getFinancialValue( 'salary_monthly' ) - totalExpenses;

    updateExpensesView();
  },

  /**
   * setValue - Used to set a value
   * @param {String} name - Property name
   * @param {Number} value - New value of property
   */
  setValue: ( name, value ) => {
    expensesModel.values[name] = value;
    expensesModel.calculateTotals();
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
      Other: 'item_other',
    };

    const salary = getFinancialValue( 'salary_annual' ) || 0;
    const salaryRange = expensesModel._getSalaryRange( salary );

    for ( let key in propertyTranslator ) {
      const value = stringToNum( expensesModel.rawData[key][region][salaryRange] );
      expensesModel.values[propertyTranslator[key]] = Math.round( value / 12 );
    }

    if ( typeof expensesModel.values.item_childcare === 'undefined' ) {
      expensesModel.values.item_childcare = 0;
    }
    expensesModel.calculateTotals();
    updateExpensesView();
  },

  /**
   * Initialize the model, fetch values from API 
   */
  init: function() {
    getExpenses()
      .then( resp => {
        expensesModel.rawData = JSON.parse( resp.responseText );
        expensesModel.setValuesByRegion( 'NE' );
        updateExpensesView();
      } );
  }


};

export {
  expensesModel
};
