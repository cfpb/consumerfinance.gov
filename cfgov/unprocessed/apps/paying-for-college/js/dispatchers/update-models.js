/**
 * Update the values of models
 */

import { expensesModel } from '../models/expenses-model.js';
import { financialModel } from '../models/financial-model.js';
import { financialView } from '../views/financial-view.js';
import { getSchoolData } from '../dispatchers/get-api-values.js';
import { schoolModel } from '../models/school-model.js';
import { schoolView } from '../views/school-view.js';
import { stringToNum } from '../util/number-utils.js';
import { getConstantsValue, getSchoolValue, getStateValue } from '../dispatchers/get-model-values.js';
import { updateGradMeterChart, updateRepaymentMeterChart } from '../dispatchers/update-view.js';

/**
  * updateFinancial - Update a property of the financial model
  * @param {String} name - The name of the property to update
  * @param {} value - The new value of the property
  */

function updateFinancial( name, value ) {
  financialModel.setValue( name, value );
}

function createFinancial( name, value ) {
  financialModel.createFinancialProperty( name, value );
}

function recalculateFinancials() {
  financialModel.recalculate();
}

function updateExpense( name, value ) {
  expensesModel.setValue( name, value );
}

function recalculateExpenses() {
  expensesModel.calculateTotals();
}

const updateSchoolData = function( iped ) {
  return new Promise( ( resolve, reject ) => {
    getSchoolData( iped )
      .then( resp => {
        const data = JSON.parse( resp.responseText );

        for ( const key in data ) {
          schoolModel.setValue( key, data[key] );
        }

        financialModel.setValue( 'salary_annual', stringToNum( getSchoolValue( 'medianAnnualPay6Yr' ) ) );
        financialModel.setValue( 'salary_monthly', stringToNum( getSchoolValue( 'medianAnnualPay6Yr' ) ) / 12 );

        resolve( true );

      } )
      .catch( function( error ) {
        reject( error );
        // console.log( 'An error occurred!', error );
      } );
  } );
};

/**
 * Copies usefulvalues from the schoolModel to the financialModel
 */
const updateFinancialsFromSchool = function() {
  financialModel.updateModelFromSchoolModel();
  financialView.updateFinancialItems();
};

export {
  updateFinancial,
  createFinancial,
  updateSchoolData,
  updateExpense,
  updateFinancialsFromSchool,
  recalculateFinancials,
  recalculateExpenses
};
