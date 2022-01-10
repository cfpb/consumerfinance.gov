/**
 * The file interfaces between our application and the studentDebtCalculator package
 */

import { calcInterestAtGrad, calcMonthlyPayment } from './debt-utils.js';
import { getConstantsValue, getStateValue } from '../dispatchers/get-model-values.js';
import { financialModel } from '../models/financial-model.js';
import { stringToNum } from '../util/number-utils.js';

// Please excuse some uses of underscore for code/HTML property clarity!
/* eslint camelcase: ["error", {properties: "never"}] */

/**
 * Calculate direct unsubsidized federal loan total. This involves calculating a different
 * amount borrowed each year.
 * @param {number} directSub - The amount of DIRECT subsidized borrowed the first year
 * @param {number} directUnsub - The amount of DIRECT unsubsidized borrowed the first year
 * @param {number} rateUnsub - The interest rate as a decimal
 * @param {number} programLength - Length of the program in years
 * @returns {object} An object containing the calculated debt values
 */
function calculateDirectLoanDebt( directSub, directUnsub, rateUnsub, programLength ) {
  const level = getStateValue( 'programLevel' );
  const dependency = getStateValue( 'programDependency' );
  const progressMap = {
    n: 0,
    a: 2
  };
  const yearMap = {
    n: 'yearOne',
    0: 'yearOne',
    1: 'yearTwo',
    a: 'yearThree',
    2: 'yearThree'
  };
  let progress = getStateValue( 'programProgress' );
  let percentSub = 1;
  let percentUnsub = 1;
  let subPrincipal = 0;
  let unsubPrincipal = 0;
  let unsubInterest = 0;
  const subCaps = getConstantsValue( 'subCaps' );
  let totalCaps = {};

  if ( level === 'undergrad' && dependency === 'dependent' ) {
    totalCaps = getConstantsValue( 'totalCaps' );
  } else if ( level === 'undergrad' && dependency === 'independent' ) {
    totalCaps = getConstantsValue( 'totalIndepCaps' );
  } else if ( level === 'graduate' ) {
    const gradCap = getConstantsValue( 'unsubsidizedCapGrad' );
    totalCaps = {
      yearOne: gradCap,
      yearTwo: gradCap,
      yearThree: gradCap
    };
  }

  // Determine percent of borrowing versus caps
  percentSub = directSub / subCaps[yearMap[progress]];
  percentUnsub = directUnsub / totalCaps[yearMap[progress]];

  /* Iterate through each year of the program
     Note that "progress" refers to number of years completed, thus a user has 0 progress
     until they start their second year. An associate's degree represents 2 years of school,
     so when progress = 'a' (for Associates), then progress is set to '2' */

  // Translate progress value to number where necessary
  if ( progressMap.hasOwnProperty( progress ) ) {
    progress = progressMap[progress];
  }

  for ( let x = 0; x < programLength; x++ ) {
    const progressNumber = stringToNum( progress ) + x;
    if ( progressNumber === 0 ) {
      subPrincipal += directSub;
      unsubPrincipal += directUnsub;
      unsubInterest += directUnsub * rateUnsub * programLength;
    } else if ( progressNumber === 1 ) {
      const subAmount = percentSub * subCaps.yearTwo;
      const unsubAmount = percentUnsub * totalCaps.yearTwo;
      subPrincipal += subAmount;
      unsubPrincipal += unsubAmount;
      unsubInterest += unsubAmount * rateUnsub * ( programLength - x );
    } else {
      const subAmount = percentSub * subCaps.yearThree;
      const unsubAmount = percentUnsub * totalCaps.yearThree;
      subPrincipal += subAmount;
      unsubPrincipal += unsubAmount;
      unsubInterest += unsubAmount * rateUnsub * ( programLength - x );
    }
  }

  return {
    subPrincipal: subPrincipal,
    unsubPrincipal: unsubPrincipal,
    unsubInterest: unsubInterest
  };
}

/**
 * Calculate debts based on financial values
 */
function debtCalculator() {
  const fedLoans = [ 'directSub', 'directUnsub' ];
  const plusLoans = [ 'gradPlus', 'parentPlus' ];
  const publicLoans = [ 'state', 'institutional', 'nonprofit' ];
  const privateLoans = [ 'privateLoan1' ];
  const newLoans = fedLoans.concat( plusLoans, publicLoans, privateLoans );
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
  let totalBorrowing = 0;

  // Find federal DIRECT debts at graduation
  const fedLoanTotals = calculateDirectLoanDebt(
    fin.fedLoan_directSub,
    fin.fedLoan_directUnsub,
    fin.rate_directUnsub,
    fin.other_programLength
  );

  debts.directSub = fedLoanTotals.subPrincipal;
  debts.directUnsub = fedLoanTotals.unsubPrincipal + fedLoanTotals.unsubInterest;
  interest.directSub = 0;
  interest.directUnsub = fedLoanTotals.unsubInterest;
  totalBorrowing += fedLoanTotals.subPrincipal + fedLoanTotals.unsubPrincipal;

  // Calculate Plus loan debts
  plusLoans.forEach( key => {
    let principal = fin['plusLoan_' + key] * fin.other_programLength;
    let int = calcInterestAtGrad(
      fin['plusLoan_' + key],
      fin['rate_' + key],
      fin.other_programLength );

    if ( isNaN( int ) ) {
      int = 0;
    }

    // if parentPlus loan, check if debt should be included
    if ( key === 'parentPlus' && !getStateValue( 'includeParentPlus' ) ) {
      principal = 0;
      int = 0;
    }

    totalBorrowing += principal;
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

    totalBorrowing += principal;
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

    totalBorrowing += principal;
    debts[key] = int + principal;
    interest[key] = int;
  } );

  newLoans.forEach( key => {
    interest.totalAtGrad += interest[key];
    debts.totalAtGrad += debts[key];

    // 10 year term calculations
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

  // set the program-level debts before current debt is added
  debts.programInterestAtGrad = interest.totalAtGrad;
  debts.programDebtAtGrad = debts.totalAtGrad;

  // calculate existing loan debt interest during program

  let existingDebtInterest = fin.existingDebt_amount * fin.rate_existingDebt * fin.other_programLength;

  if ( isNaN( existingDebtInterest ) ) {
    existingDebtInterest = 0;
  }

  const existingDebtTotalAtGrad = fin.existingDebt_amount + existingDebtInterest;
  const existingDebtMonthly = calcMonthlyPayment(
    existingDebtTotalAtGrad, fin.rate_existingDebt, 10 );

  debts.existingDebtInterestAtGrad = existingDebtInterest;

  totalBorrowing += fin.existingDebt_amount;
  interest.totalAtGrad += existingDebtInterest;
  debts.totalAtGrad += existingDebtTotalAtGrad;

  debts.tenYearMonthly += existingDebtMonthly;
  debts.tenYearTotal += existingDebtMonthly * 120;

  // Calculate totals
  debts.totalInterestAtGrad = interest.totalAtGrad;
  debts.tenYearInterest = debts.tenYearTotal - debts.totalAtGrad - existingDebtInterest;

  debts.twentyFiveYearInterest = debts.twentyFiveYearTotal - debts.totalAtGrad;
  debts.repayHours = debts.tenYearMonthly / 15;
  debts.repayWorkWeeks = debts.repayHours / 40;

  fin.total_borrowingAtGrad = totalBorrowing;
  for ( const key in debts ) {
    fin['debt_' + key] = debts[key];
  }
}


export {
  debtCalculator
};
