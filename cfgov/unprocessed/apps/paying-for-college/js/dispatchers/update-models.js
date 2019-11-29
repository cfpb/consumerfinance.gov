/**
 * Update the values of models
 */

import { expensesModel } from '../models/expenses-model.js';
import { financialModel } from '../models/financial-model.js';
import { financialView } from '../views/financial-view.js';
import { schoolModel } from '../models/school-model.js';
import { getSchoolData } from '../dispatchers/get-api-values.js';
import { getState } from '../dispatchers/get-state.js';
import { getConstantsValue, getSchoolValue } from '../dispatchers/get-model-values.js';

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

const updateSchoolData = function( iped ) {
  getSchoolData( iped )
    .then( resp => {
      const data = JSON.parse( resp.responseText );

      for ( const key in data ) {
        schoolModel.createSchoolProperty( key, data[key] );
      }

      financialModel.setValue( 'salary_annual', Number( getSchoolValue( 'schoolSalary' ) ) );
      financialModel.setValue( 'salary_monthly', Number( getSchoolValue( 'schoolSalary' ) ) / 12 );

      financialView.updateFinancialItems();
    } );
};

/**
 * Copies usefulvalues from the schoolModel to the financialModel
 */
const importSchoolToFinancial = function() {
  const program = getState( 'programData' );

  if ( program.type === 'graduate' ) {
    if ( program.rate === 'out-of-state' ) {
      financialModel.setValue( 'dirCost_tuition', Number( getSchoolValue( 'tuitionGradOss' ) ) );
    } else if ( program.rate === 'in-state' ) {
      financialModel.setValue( 'dirCost_tuition', Number( getSchoolValue( 'tuitionGradInS' ) ) );
    } else if ( program.rate === 'in-district' ) {
      financialModel.setValue( 'dirCost_tuition', Number( getSchoolValue( 'tuitionGradInDis' ) ) );
    }
  } else if ( program.rate === 'out-of-state' ) {
    financialModel.setValue( 'dirCost_tuition', Number( getSchoolValue( 'tuitionUnderOoss' ) ) );
  } else if ( program.rate === 'in-state' ) {
    financialModel.setValue( 'dirCost_tuition', Number( getSchoolValue( 'tuitionUnderInS' ) ) );
  } else if ( program.rate === 'in-district' ) {
    financialModel.setValue( 'dirCost_tuition', Number( getSchoolValue( 'tuitionUnderInDis' ) ) );
  }

  if ( program.housing === 'on-campus' ) {
    financialModel.setValue( 'dirCost_housing', Number( getSchoolValue( 'roomBrdOnCampus' ) ) );
    financialModel.setValue( 'indiCost_other', Number( getSchoolValue( 'otherOnCampus' ) ) );
  } else if ( program.housing === 'off-campus' ) {
    financialModel.setValue( 'dirCost_housing', Number( getSchoolValue( 'roomBrdOffCampus' ) ) );
    financialModel.setValue( 'indiCost_other', Number( getSchoolValue( 'otherOffCampus' ) ) );
  } else if ( program.housing === 'with-family' ) {
    financialModel.setValue( 'dirCost_housing', Number( getSchoolValue( 'roomBrdOffCampus' ) ) );
    financialModel.setValue( 'indiCost_other', Number( getSchoolValue( 'otherWFamily' ) ) );
  }

  financialModel.setValue( 'indiCost_books', Number( getSchoolValue( 'books' ) ) );

  financialView.updateFinancialItems();

};

export {
  updateFinancial,
  createFinancial,
  updateSchoolData,
  importSchoolToFinancial
};
