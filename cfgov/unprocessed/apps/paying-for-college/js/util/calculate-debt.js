/**
 * The file interfaces between our application and the studentDebtCalculator package
 */

import studentDebtCalculator from 'student-debt-calc';
import { financialModel } from '../models/financial-model.js';
import { constantsModel } from '../models/constants-model.js';
import { getFinancialValue, getStateValue } from '../dispatchers/get-model-values.js';

// Please excuse some uses of underscore for code/HTML property clarity!
/* eslint camelcase: ["error", {properties: "never"}] */

const calculateDebt = function( data ) {
  let values = {};

  const debtObj = {
    debt_totalAtGrad: 0,
    debt_tenYearTotal: 0,
    debt_tenYearMonthly: 0,
    debt_tenYearInterest: 0,
    debt_twentyFiveYearTotal: 0,
    debt_twentyFiveYearMonthly: 0,
    debt_twentyFiveYearInterest: 0
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

  for ( const key in modelToCalc ) {
    values[modelToCalc[key]] = getFinancialValue( key );
  }

  // 'directPlus' is to avoid a bug in studentDebtCalc
  values.directPlus = 0;

  // Add additional values
  values.programLength = getStateValue( 'programLength' );
  values.undergraduate = getStateValue( 'programType' ) !== 'graduate';
  values.program = getStateValue( 'programType' ) === 'graduate' ? 'grad' : 'ba';

  values = studentDebtCalculator( values );

  debtObj.debt_totalAtGrad = Math.round( values.totalDebt );

  // Ten year term
  debtObj.debt_tenYearTotal = Math.round( values.tenYear.loanLifetime );
  debtObj.debt_tenYearMonthly = Math.round( values.tenYear.loanMonthly );
  debtObj.debt_tenYearInterest = Math.round( values.tenYear.loanLifetime - values.total_borrowingAtGrad );

  // Twenty-five year term
  debtObj.debt_twentyFiveYearTotal = Math.round( values.twentyFiveYear.loanLifetime );
  debtObj.debt_twentyFiveYearMonthly = Math.round( values.twentyFiveYear.loanMonthly );
  debtObj.debt_twentyFiveYearInterest = Math.round( values.twentyFiveYear.loanLifetime - values.total_borrowingAtGrad );

  return debtObj;
};

export {
  calculateDebt
};
