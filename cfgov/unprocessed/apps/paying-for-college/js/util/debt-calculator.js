/**
 * The file interfaces between our application and the studentDebtCalculator package
 */

import studentDebtCalculator from 'student-debt-calc';
import { calcDebtAtGrad, calcMonthlyPayment } from './debt-utils.js';
import { getConstantsValue, getFinancialValue, getStateValue } from '../dispatchers/get-model-values.js';
import { constantsModel } from '../models/constants-model.js';
import { financialModel } from '../models/financial-model.js';
import { updateFinancial, updateFinancialsFromSchool } from '../dispatchers/update-models.js';

// Please excuse some uses of underscore for code/HTML property clarity!
/* eslint camelcase: ["error", {properties: "never"}] */

/**
 * Calculate debts based on financial values
 */
function debtCalculator() {
  const fedLoans = [ 'directSub', 'directUnsub' ];
  const plusLoans = [ 'gradPlus', 'parentPlus' ];
  const publicLoans = [ 'state', 'institutional', 'nonprofit' ];
  const privateLoans = [ 'privateLoan1' ];
  const allLoans = fedLoans.concat( plusLoans, publicLoans, privateLoans );
  const fin = financialModel.values;
  const debts = {
    totalAtGrad: 0,
    tenYearTotal: 0,
    tenYearMonthly: 0,
    tenYearInterest: 0,
    twentyFiveYearTotal: 0,
    twentyFiveYearMonthly: 0,
    twentyFiveYearInterest: 0
  };

  // Find federal debts at graduation
  fedLoans.forEach( key => {
    // DIRECT Subsidized loans are special
    let val = 0;
    if ( key === 'directSub' ) {
      val = fin['fedLoan_' + key] * fin.other_programLength;
    } else {
      val = calcDebtAtGrad( fin['fedLoan_' + key],
        fin['rate_' + key], fin.other_programLength, 6 );
    }

    if ( isNaN( val ) ) {
      val = 0;
    }
    debts[key] = val;
  } );

  plusLoans.forEach( key => {
    let val = calcDebtAtGrad(
      fin['plusLoan_' + key],
      fin['rate_' + key],
      fin.other_programLength,
      6 );

    if ( isNaN( val ) ) {
      val = 0;
    }
    debts[key] = val;
  } );

  // calculate debts of other loans

  publicLoans.forEach( key => {
    let val = calcDebtAtGrad(
      fin['publicLoan_' + key],
      fin['rate_' + key],
      fin.other_programLength,
      0
    );

    if ( isNaN( val ) ) {
      val = 0;
    }
    debts[key] = val;

  } );

  privateLoans.forEach( key => {
    let val = calcDebtAtGrad(
      fin['privLoan_' + key],
      fin['rate_' + key],
      fin.other_programLength,
      0
    );

    if ( isNaN( val ) ) {
      val = 0;
    }
    debts[key] = val;

  } );

  // 10 year term calculations.
  allLoans.forEach( key => {
    debts.totalAtGrad += debts[key];
    let tenYearMonthly = calcMonthlyPayment(
      debts[key],
      fin['rate_' + key],
      10
    );

    if ( isNaN( tenYearMonthly ) ) {
      tenYearMonthly = 0;
    }

    /* debts[ key + '_tenYearMonthly' ] = tenYearMonthly;
       debts[ key + '_tenYearTotal' ] = tenYearMonthly * 120;
       debts[ key + '_tenYearInterest' ] = (tenYearMonthly * 120 ) - debts[key]; */
    debts.tenYearMonthly += tenYearMonthly;
    debts.tenYearTotal += tenYearMonthly * 120;

    // 25 year term calculations
    let twentyFiveYearMonthly = calcMonthlyPayment(
      debts[key],
      fin['rate_' + key],
      10
    );

    if ( isNaN( twentyFiveYearMonthly ) ) {
      twentyFiveYearMonthly = 0;
    }

    /* debts[ key + '_twentyFiveYearMonthly' ] = twentyFiveYearMonthly;
       debts[ key + '_twentyFiveYearTotal' ] = twentyFiveYearMonthly * 300;
       debts[ key + '_twentyFiveYearInterest' ] = ( twentyFiveYearMonthly * 300 ) - debts[key]; */
    debts.twentyFiveYearMonthly += twentyFiveYearMonthly;
    debts.twentyFiveYearTotal += twentyFiveYearMonthly * 300;

  } );

  debts.tenYearInterest = debts.tenYearTotal - debts.totalAtGrad;
  debts.twentyFiveYearInterest = debts.twentyFiveYearTotal - debts.totalAtGrad;
  debts.repayHours = debts.tenYearMonthly / 15;
  debts.repayWorkWeeks = debts.repayHours / 40;
  debts.programInterest = debts.totalAtGrad - fin.total_borrowingAtGrad;

  // TODO: Differentiate grads versus undergrads

  // TODO: Apply the changing-over-time DIRECT maxes to DIRECT borrowing

  // TODO: Toggle for parentPlus debt

  for ( const key in debts ) {
    fin['debt_' + key] = debts[key];
  }

}


export {
  debtCalculator
};
