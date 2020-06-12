/**
 * calcDebtAtGrad - Calculate debt at end of program length (graduation)
 * @param {Number} amount - Amount of loan per year
 * @param {Number} rate - Interest rate (as decimal)
 * @param {Number} programLength - Program length in years
 * @param {Number} deferPeriod - Deferral period, in months
 * @returns {Number} total debt at end of programLength
 */
function calcDebtAtGrad( amount, rate, programLength, deferPeriod ) {

  const total = amount * rate / 12 *
    ( ( programLength * ( programLength + 1 ) / 2 *
    12 + programLength * deferPeriod ) ) +
    amount * programLength;

  return total;

}

/**
 * calcMonthlyPayment - Calculate monthly payment of loan after term
 * @param {Number} debt - Amount of debt at end of program
 * @param {Number} rate - Interest rate, as decimal
 * @param {Number} term - Loan term, in years
 * @returns {Number} monthly payment of loan for term
 */
function calcMonthlyPayment( debt, rate, term ) {
  let monthly = 0;

  if ( rate === 0 ) {
    monthly = debt / ( term * 12 );
  } else {
    monthly = debt * ( rate / 12 ) /
      ( 1 - Math.pow( 1 + rate / 12, -1 * term * 12 ) );
  }

  return monthly;
}

export {
  calcDebtAtGrad,
  calcMonthlyPayment
};
