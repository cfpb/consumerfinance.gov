/**
 * Recalculates the student debt totals, etc
 */

import studentDebtCalculator from 'student-debt-calc';
import { financialModel } from '../models/financial-model.js';
import { constantsModel } from '../models/constants-model.js';
import { financialView } from '../views/financial-view.js';
import { getState } from '../dispatchers/get-state.js';
import { getSchoolValue, getFinancialValue } from '../dispatchers/get-model-values.js';


const recalculate = function() {
  let values = {};
  const modelToCalc = {
    total_costs: 'tuitionFees',
    total_grantsScholarships: 'scholarships',
    total_otherResources: 'savings',
    fedLoan_directSub: 'directSubsidized',
    fedLoan_directUnsub: 'directUnsubsidized',
    privloan_school: 'privateLoan',
    rate_schoolLoan: 'privateLoanRate',
  };
  const calcToModel = {
    
  }

  values = Object.assign( constantsModel.values );
  for ( let key in values ) {
    values[key] = Number( values[key] );
  }
  for ( let key in translations ) {
    values[translations[key]] = getFinancialValue( key );
  }

  values.directSubsidized = 19000;

  // Add additional values
  values.programLength = getState( 'program' ).length;

  values = studentDebtCalculator( values );

  console.log( values );

}

export {
    recalculate
}