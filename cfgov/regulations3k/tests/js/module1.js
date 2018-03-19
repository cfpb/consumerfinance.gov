
var chai = require('chai');
var expect = require('chai').expect;

var loanCalculator = require( '../../js/module1.js' );

describe( 'Loan calculator helps users calculate loan data', function() {

  it( 'should not throw any errors on init', function() {
    expect( () => loanCalculator.init() ).to.not.throw();
  });

  it( 'should calculate a loan\'s monthly payment', function() {
    expect( loanCalculator.getMonthlyPayment( 180000, 4.25, 360, 60 ) ).to.equal( 885.4918039430557 );
  });

});
