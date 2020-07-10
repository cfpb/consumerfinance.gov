/**
 * The file interfaces between our application and the studentDebtCalculator package
 */

import studentDebtCalculator from 'student-debt-calc';
import { calcInterestAtGrad, calcMonthlyPayment } from './debt-utils.js';
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
  const interest = {
    totalAtGrad: 0
  };

  // Find federal debts at graduation
  fedLoans.forEach( key => {
    // DIRECT Subsidized loans are special
    let int = 0;
    const principal = fin['fedLoan_' + key] * fin.other_programLength;
    if ( key === 'directSub' ) {
      int = 0;
    } else {
      int = calcInterestAtGrad( fin['fedLoan_' + key],
        fin['rate_' + key], fin.other_programLength );
    }

    if ( isNaN( int ) ) {
      int = 0;
    }
    debts[key] = int + principal;
    interest[key] = int;
  } );

  plusLoans.forEach( key => {
    const principal = fin['plusLoan_' + key] * fin.other_programLength;
    let int = calcInterestAtGrad(
      fin['plusLoan_' + key],
      fin['rate_' + key],
      fin.other_programLength );

    if ( isNaN( int ) ) {
      int = 0;
    }

    debts[key] = int + principal;
    interest[key] = int;
  } );

  // calculate debts of other loans

  publicLoans.forEach( key => {
    const principal = fin['publicLoan_' + key] * fin.other_programLength;
    let int = calcInterestAtGrad(
      fin['publicLoan_' + key],
      fin['rate_' + key],
      fin.other_programLength );

    if ( isNaN( int ) ) {
      int = 0;
    }

    debts[key] = int + principal;
    interest[key] = int;
  } );

  privateLoans.forEach( key => {
    const principal = fin['privLoan_' + key] * fin.other_programLength;
    let int = calcInterestAtGrad(
      fin['privLoan_' + key],
      fin['rate_' + key],
      fin.other_programLength );

    if ( isNaN( int ) ) {
      int = 0;
    }

    debts[key] = int + principal;
    interest[key] = int;
  } );

  // 10 year term calculations.
  allLoans.forEach( key => {
    interest.totalAtGrad += interest[key];
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

  debts.programInterest = interest.totalAtGrad;
  debts.tenYearInterest = debts.tenYearTotal - debts.totalAtGrad;
  debts.twentyFiveYearInterest = debts.twentyFiveYearTotal - debts.totalAtGrad;
  debts.repayHours = debts.tenYearMonthly / 15;
  debts.repayWorkWeeks = debts.repayHours / 40;

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
