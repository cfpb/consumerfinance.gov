/**
 * Update the values of models
 */

import { expensesModel } from '../models/expenses-model.js';
import { financialModel } from '../models/financial-model.js';
import { financialView } from '../views/financial-view.js';
import { schoolView } from '../views/school-view.js';
import { schoolModel } from '../models/school-model.js';
import { getSchoolData } from '../dispatchers/get-api-values.js';
import { getConstantsValue, getSchoolValue, getStateValue } from '../dispatchers/get-model-values.js';
import { updateGradMeterChart, updateRepaymentMeterChart } from '../dispatchers/update-view.js';

/**
  * updateFinancial - Update a property of the financial model
  * @param {String} name - The name of the property to update
  * @param {} value - The new value of the property
  */

const updateFinancial = function( name, value ) {
  financialModel.setValue( name, value );
};

const createFinancial = function( name, value ) {
  financialModel.createFinancialProperty( name, value );
};

const recalculateFinancials = () => {
  financialModel.recalculate();
};

const updateExpense = function( name, value ) {
  expensesModel.setValue( name, value );
};

const updateSchoolData = function( iped ) {
  getSchoolData( iped )
    .then( resp => {
      const data = JSON.parse( resp.responseText );

      for ( const key in data ) {
        schoolModel.createSchoolProperty( key, data[key] );
      }

      financialModel.setValue( 'salary_annual', Number( getSchoolValue( 'medianAnnualPay6Yr' ) ) );
      financialModel.setValue( 'salary_monthly', Number( getSchoolValue( 'medianAnnualPay6Yr' ) ) / 12 );

      financialView.updateFinancialItems();
      updateGradMeterChart();
      updateRepaymentMeterChart();
      schoolView.updateSchoolRadioButtons();

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
  updateFinancialsFromSchool,
  recalculateFinancials
};
