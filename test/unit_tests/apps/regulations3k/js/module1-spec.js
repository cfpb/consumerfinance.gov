const BASE_JS_PATH = '../../../../../cfgov/unprocessed/apps/regulations3k';

const loanCalculator = require( `${ BASE_JS_PATH }/js/module1.js` );

describe( 'Loan calculator helps users calculate loan data', () => {

  it( 'should not throw any errors on init', () => {
    expect( () => loanCalculator.init() ).not.toThrow();
  } );

  it( 'should calculate a loan\'s monthly payment', () => {
    const payment = loanCalculator.getMonthlyPayment( 180000, 4.25, 360, 60 );
    expect( payment ).toBe( 885.4918039430557 );
  } );

} );
