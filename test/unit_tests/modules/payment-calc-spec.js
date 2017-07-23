'use strict';

const BASE_OAH_JS_PATH = require( '../../config' ).BASE_OAH_JS_PATH;
const payment = require( BASE_OAH_JS_PATH + '/modules/payment-calc.js' );

const chai = require( 'chai' );
const expect = chai.expect;

describe( 'Payment calculation tests', function() {
  it( 'Positive test - correctly calculates a monthly payment on 20 year loan', function() {
    expect( payment( 5, 240, 200000 ) ).to.equal( '$1,319.91' );
  } );

  it( 'Positive test - correctly calculates a monthly payment on 30 year loan', function() {
    expect( payment( 5, 360, 200000 ) ).to.equal( '$1,073.64' );
  } );

// -- LOAN RATE TESTS -- //
  it( 'Negative test - passes *Decimal* Loan Rate', function() {
    expect( payment( 3.6, 240, 200000 ) ).to.equal( '$1,170.22' );
  } );

  // --- GH Issue 279 - https://fake.ghe.domain/OAH/OAH-notes/issues/279 --- //
  // Should we allow ZERO as a valid loan rate? should we throw an exception?
  it( 'Negative test - passes *Zero* Loan Rate', function() {
    expect( payment( 0, 240, 200000 ) ).to.equal( '$0.00' );
  } );

  // --- GH Issue 279 - https://fake.ghe.domain/OAH/OAH-notes/issues/279 --- //
  // This test should catch the exception: Error: Please specify a loan rate as a number between 1 and 99
  it( 'Negative test - passes *Out of range* Loan Rate argument', function() {
    expect( payment( 999, 240, 500000 ) ).to.equal( '$416,250.00' );
  } );

  // --- GH Issue 278 - https://fake.ghe.domain/OAH/OAH-notes/issues/278 --- //
  // This test should catch the exception: Error: Please specify a loan rate as a number
  /* it('Negative test - passes a *Negative* Loan Rate', function() {
    expect(payment(-5, 240, 200000)).to.equal('$1,319.91');
  });
  */

  // This test should catch the exception: Error: Please specify a loan rate as a number
  /* it('Negative test - passes an *Invalid* Loan Rate', function() {
    expect(payment('&', 240, 200000)).to.equal('$1,319.91');
  });
  */

// -- LOAN TERM TESTS -- //
  it( 'Negative test - passes a *Decimal* Loan Term', function() {
    expect( payment( 5, 360.1, 200000 ) ).to.equal( '$1,073.51' );
  } );

  // --- GH Issue 278 - https://fake.ghe.domain/OAH/OAH-notes/issues/278 --- //
  // This test should catch the exception: Error: Please specify the length of the loan term as a positive number
  /* it('Negative test - passes *ZERO* Loan Term', function() {
    expect(payment(5, 0, 200000)).to.equal('$1,073.51');
  });
  */

  // This test should cause an exception: Error: Please specify a loan term as a number between 1 and 480
  it( 'Negative test - passes *Out of range* Loan Term argument', function() {
    expect( payment( 5, 600, 300000 ) ).to.equal( '$1,362.42' );
  } );

  // --- GH Issue 278 - https://fake.ghe.domain/OAH/OAH-notes/issues/278 --- //
  // This test should catch the exception: Error: Please specify the length of the term as a positive number
  /* it('Negative test - passes a *Negative* Loan Term', function() {
    expect(payment(5, -240, 200000)).to.equal('$1,319.91');
  });
  */

  // --- GH Issue 278 - https://fake.ghe.domain/OAH/OAH-notes/issues/278 --- //
  // This test should catch the exception: Error: Please specify the length of the term as a positive number
  /* it('Negative test - passes an *Invalid* Loan Term', function() {
    expect(payment(7, '*', 200000)).to.equal('$1,319.91');
  });
  */

// -- LOAN AMOUNT TESTS -- //
  it( 'Negative test - passes *Decimal* Loan Amount', function() {
    expect( payment( 3.6, 480, 200000.05 ) ).to.equal( '$786.82' );
  } );

  // --- GH Issue 278 - https://fake.ghe.domain/OAH/OAH-notes/issues/278 --- //
  // This test should catch the exception: Error: Please specify a loan amount as a positive number
  /* it('Negative test - passes *Zero* Loan Amount', function() {
    expect(payment(3.6, 480, 0)).to.equal('$786.82');
  });
  */

  // --- GH Issue 278 - https://fake.ghe.domain/OAH/OAH-notes/issues/278 --- //
  // This test should catch the exception: Error: Please specify a loan amount as a positive number
  /* it('Negative test - passes *Negative* Loan Amount', function() {
    expect(payment(3.6, 480, -180000)).to.equal('$786.82');
  });
  */

  // --- GH Issue 278 - https://fake.ghe.domain/OAH/OAH-notes/issues/278 --- //
  // This test should catch the exception: Error: Please specify a loan amount as a positive number
  /* it('Negative test - passes an *Invalid* Loan Amount', function() {
    expect(payment(3.6, 480, '%')).to.equal('$786.82');
  });
  */

} );
