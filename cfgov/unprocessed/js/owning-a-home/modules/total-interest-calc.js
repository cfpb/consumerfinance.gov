'use strict';

var LoanCalc = require( 'loan-calc' );
var formatUSD = require( 'format-usd' );

/**
 * Calculate the total interest paid on a loan.
 * @param {number} loanRate - The loan rate.
 * @param {number} termLength - The loan term length.
 * @param {number} loanAmt - The loan amount.
 * @returns {number} Total interest paid on a loan.
 */
function calcInterest( loanRate, termLength, loanAmt ) {
  var totalInterest = LoanCalc.totalInterest( {
    amount: loanAmt,
    rate: loanRate,
    termMonths: termLength
  } );
  return formatUSD( totalInterest );
}

module.exports = calcInterest;
