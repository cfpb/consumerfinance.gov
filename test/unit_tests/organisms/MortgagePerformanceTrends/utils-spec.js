'use strict';

const BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';

const chai = require( 'chai' );
const mockery = require( 'mockery' );
const expect = chai.expect;

// Disable the AJAX library used by the action creator
const noop = () => ( {} );
mockery.enable( {
  warnOnReplace: false,
  warnOnUnregistered: false
} );
mockery.registerMock( 'xdr', noop );

const utils = require( BASE_JS_PATH + 'organisms/MortgagePerformanceTrends/utils.js' );

let el;

describe( 'Mortgage Performance utilities', () => {

  beforeEach( () => {
    el = {
      style: {}
    };
  } );

  it( 'should clear an element\'s diplay property', () => {
    utils.showEl( el );
    expect( el.style.display ).to.equal( '' );
  } );

  it( 'should set an element\'s diplay property', () => {
    utils.hideEl( el );
    expect( el.style.display ).to.equal( 'none' );
  } );

  it( 'should parse date strings', () => {
    let date = utils.getDate( '2009-01-01' );
    expect( date ).to.equal( 'January 2009' );
    date = utils.getDate( '2020-11-27' );
    expect( date ).to.equal( 'November 2020' );
    date = utils.getDate( 'cheeseburger' );
    expect( date ).to.equal( 'cheeseburger' );
  } );

  it( 'check if a FIPS is a non-metro area', () => {
    let location = utils.isNonMetro( '87364' );
    expect( location ).to.be.false;
    location = utils.isNonMetro( '1234567890' );
    expect( location ).to.be.false;
    location = utils.isNonMetro( '06-non' );
    expect( location ).to.be.true;
    location = utils.isNonMetro( 'non-06' );
    expect( location ).to.be.false;
  } );

} );
