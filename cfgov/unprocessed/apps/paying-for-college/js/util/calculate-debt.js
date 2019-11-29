/**
 * The file interfaces between our application and the studentDebtCalculator package
 */

import studentDebtCalculator from 'student-debt-calc';
import { financialModel } from '../models/financial-model.js';
import { constantsModel } from '../models/constants-model.js';
import { getState } from '../dispatchers/get-state.js';
import { getFinancialValue } from '../dispatchers/get-model-values.js';

const calculateDebt = function( data ) {
  let values = {};
  const debtObj = {
    total_debtAtGrad: 0,
    total_debt10year: 0,
    total_debtMonthly10year: 0,
    total_interest10yr: 0
  };
  const modelToCalc = {
    total_costs: 'tuitionFees',
    total_grantsScholarships: 'scholarships',
    total_otherResources: 'savings',
    fedLoan_directSub: 'directSubsidized',
    fedLoan_directUnsub: 'directUnsubsidized',
    privloan_school: 'privateLoan',
    rate_schoolLoan: 'privateLoanRate',
    instiLoan_institutional: 'institutionalLoan',
    rate_institutionalLoan: 'institutionalLoanRate'
  };

  values = Object.assign( constantsModel.values, data );

  console.log( 'after merge', values );

  for ( const key in modelToCalc ) {
    values[modelToCalc[key]] = getFinancialValue( key );
  }

  // 'directPlus' is to avoid a bug in studentDebtCalc
  values.directPlus = 0;

  // Add additional values
  values.programLength = getState( 'program' ).length;
  values.undergraduate = getState( 'program' ).type !== 'graduate';
  values.program = getState( 'program' ).type === 'graduate' ? 'grad' : 'ba';

  console.log( 'before calc: ', values.DLOriginationFee );

  values = studentDebtCalculator( values );

  /* Copy over debt values
     TODO: Take out the +1 on the next line */
  debtObj.total_debtAtGrad = values.totalDebt;
  debtObj.total_debt10year = values.tenYear.loanLifetime;
  debtObj.total_debtMonthly10year = values.tenYear.loanMonthly;
  debtObj.total_interest10year = values.tenYear.loanLifetime - values.borrowingTotal;
  debtObj.total_debtRuleGap = values.totalDebt - values.salary_annual;

  return debtObj;
};

export {
  calculateDebt
};
