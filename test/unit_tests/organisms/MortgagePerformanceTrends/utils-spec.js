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
let document = {
  createElement: () => ( {} )
};

describe( 'Mortgage Performance utilities', () => {

  beforeEach( () => {
    el = {
      style: {},
      disabled: false
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

  it( 'should disable an element', () => {
    utils.disableEl( el );
    expect( el.disabled ).to.be.true;
  } );

  it( 'should un-disable an element', () => {
    utils.enableEl( el );
    expect( el.disabled ).to.be.false;
  } );

  it( 'should be able to create a select option', () => {
    const option = utils.addOption( {
      document,
      value: 'AL',
      text: 'Alabama',
      selected: false
    } );
    expect( option ).to.deep.equal( { value: 'AL', text: 'Alabama' } );
  } );

  it( 'should be able to calculate zoom levels', () => {
    // Not a pure function. The following behavior is expected.
    expect( utils.getZoomLevel( 5 ) ).to.equal( 0.5 );
    expect( utils.getZoomLevel( 5 ) ).to.equal( 1 );
  } );

  it( 'should be able to set zoom levels', () => {
    expect( utils.setZoomLevel( 5 ) ).to.equal( 5 );
    expect( utils.setZoomLevel( 7 ) ).to.equal( 7 );
    expect( utils.setZoomLevel( 234.56 ) ).to.equal( 234.56 );
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
