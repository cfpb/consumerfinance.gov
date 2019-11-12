/**
 * Update the values of models
 */

import { expensesModel } from '../models/expenses-model.js';
import { financialModel } from '../models/financial-model.js';
import { financialView } from '../views/financial-view.js';
import { schoolModel } from '../models/school-model.js';

const updateModels = {
    


}

/**
  * updateFinancial - Update a property of the financial model
  * @param {String} name - The name of the property to update
  * @param {} value - The new value of the property
  */

const updateFinancial = function( name, value ) {
    financialModel.setValue( name, value );
}

const createFinancial = function( name ) {
    financialModel.createFinancialProperty( name );
}

export {
    updateFinancial,
    createFinancial
}