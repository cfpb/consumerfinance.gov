const amortize = require( 'amortize' );

const module1 = {
  init: () => {
    console.log( 'module 1 loaded!' );
  },
  getMonthlyPayment: ( amount, rate, months, amortizeMonths ) => {
    const terms = amortize( {
      amount: amount,
      rate: rate,
      totalTerm: months,
      amortizeTerm: amortizeMonths
    } );
    return terms.payment;
  }
};

module.exports = module1;
