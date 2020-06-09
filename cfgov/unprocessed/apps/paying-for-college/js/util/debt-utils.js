function calcDebtAtGrad( amount, rate, programLength, deferPeriod ) {

  const total = amount * rate / 12 *
    ( ( programLength * ( programLength + 1 ) / 2 *
    12 + programLength * deferPeriod ) ) +
    amount * programLength;

  return total;

}

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
