/**
 * calcInterestAtGrad - Calculate interest at end of program length (graduation)
 * NOTE: This ONLY works for debts incurred once per year, each year, during the program.
 * @param {Number} amount - Amount of loan per year
 * @param {Number} rate - Interest rate (as decimal)
 * @param {Number} programLength - Program length in years
 * @returns {Number} total debt at end of programLength
 */
function calcInterestAtGrad( amount, rate, programLength ) {
  let interest = 0;

  if ( rate === 0 ) {
    return 0;
  }

  for ( let x = programLength; x > 0; x-- ) {
    interest += amount * rate * x;

  }

  return interest;
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
  calcInterestAtGrad,
  calcMonthlyPayment
};
