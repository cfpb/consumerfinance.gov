'use strict';

const BASE_OAH_JS_PATH = require( '../../config' ).BASE_OAH_JS_PATH;
const monthly = require( BASE_OAH_JS_PATH + '/modules/monthly-payment-calc.js' );

const chai = require( 'chai' );
const expect = chai.expect;
const data = {
  preTaxIncome: 5000,
  preTaxIncomeCB: 4000,
  takeHomeIncome: 3500,
  takeHomeIncomeCB: 3000,
  rent: 2000,
  utilities: 200,
  debtPayments: 1000,
  livingExpenses: 2500,
  savings: 600,
  homeMaintenance: 200,
  homeImprovement: 100,
  condoHOA: 500,
  futureUtilities: 300,
  emergencySavings: 100,
  longTermSavings: 400,
  homePrice: 300000,
  propertyTax: 1.1,
  homeownersInsurance: 750
};

describe( 'Monthly payment calculations', function() {

  describe( 'Calculates pre-tax income', function() {

    it( 'Positive test - should add positive values for income and co borrower income', function() {
      expect( monthly.preTaxIncomeTotal( data ) ).to.equal( 9000 );
    } );

  } );

  describe( 'Calculates take home income', function() {

    it( 'Positive test - should add positive values for income and co borrower take home income', function() {
      expect( monthly.takeHomeIncomeTotal( data ) ).to.equal( 6500 );
    } );

  } );

  describe( 'Calculates spending & savings', function() {

    it( 'Positive test - should add positive values for spending and savings', function() {
      expect( monthly.spendingAndSavings( data ) ).to.equal( 6300 );
    } );

  } );

  describe( 'Calculates home maintenance and improvement', function() {

    it( 'Positive test - should add positive values for home maintenance and improvement', function() {
      expect( monthly.homeMaintenanceAndImprovement( data ) ).to.equal( 300 );
    } );

  } );

  describe( 'Calculates new homeownership expenses', function() {

    it( 'Positive test - should add positive values for new homeownership expenses', function() {
      expect( monthly.newHomeownershipExpenses( data ) ).to.equal( 800 );
    } );

  } );

  describe( 'Calculates future savings', function() {

    it( 'Positive test - should add positive values for future savings', function() {
      expect( monthly.futureSavings( data ) ).to.equal( 500 );
    } );

  } );

  describe( 'Calculates available housing funds', function() {

    it( 'Positive test - should calculate available housing funds', function() {
      expect( monthly.availableHousingFunds( data ) ).to.equal( 1900 );
    } );

  } );

  describe( 'Calculates estimated total payment', function() {

    it( 'Positive test - should calculate estimated total payment', function() {
      expect( monthly.estimatedTotalPayment( data ) ).to.equal( 1400 );
    } );

  } );

  describe( 'Calculates taxes and insurance', function() {

    it( 'Positive test - should calculate taxes and insurance', function() {
      expect( monthly.taxesAndInsurance( data ) ).to.equal( 337.50000000000006 );
    } );

  } );

  describe( 'Calculates principal and interest', function() {

    it( 'Positive test - should calculate principal and interest', function() {
      expect( monthly.principalAndInterest( data ) ).to.equal( 1062.5 );
    } );

  } );

  describe( 'Calculates percentage of income available for housing expenses', function() {

    it( 'Positive test - should calculate percentage income available', function() {
      expect( monthly.percentageIncomeAvailable( data ) ).to.equal( 21 );
    } );

  } );

} );
