'use strict';

const BASE_OAH_JS_PATH = require( '../../config' ).BASE_OAH_JS_PATH;
const monthly = require( BASE_OAH_JS_PATH + '/modules/monthly-payment-calc.js' );
const payment = require( BASE_OAH_JS_PATH + '/modules/total-interest-calc.js' );

const chai = require( 'chai' );
const expect = chai.expect;

describe( 'Calculates the total interest of a loan', function() {
  it( 'Positive test - correctly calculates a the total interest over the life of a 15 year loan', function() {
    expect( payment( 2.5, 180, 100000 ) ).to.equal( '$20,022.06' );
  } );

  it( 'Positive test - correctly calculates a the total interest over the life of a 20 year loan', function() {
    expect( payment( 5, 240, 200000 ) ).to.equal( '$116,778.75' );
  } );

  it( 'Positive test - correctly calculates a the total interest over the life of a 30 year loan', function() {
    expect( payment( 3.5, 360, 400000 ) ).to.equal( '$246,624.35' );
  } );

  // --- GH Issue 278 - https://fake.ghe.domain/OAH/OAH-notes/issues/278 --- //
  // This test should catch the exception: Error: Please specify a loan rate as a number
  /* it('Negative test - passes a *Negative* loan rate', function() {
    expect(payment(-3.5, 360, 400000)).to.equal('$246,624.35');
  });
	*/

  // --- GH Issue 278 - https://fake.ghe.domain/OAH/OAH-notes/issues/278 --- //
  // This test should catch the exception: Error: Please specify a loan rate as a number
 /* it('Negative test - passes an *Invalid* loan rate', function() {
    expect(payment('*', 360, 400000)).to.equal('$246,624.35');
  });
  */
} );
