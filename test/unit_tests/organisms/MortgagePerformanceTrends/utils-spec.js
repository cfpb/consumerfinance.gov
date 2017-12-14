const BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';

const chai = require( 'chai' );
const mockery = require( 'mockery' );
const sinon = require( 'sinon' );
const expect = chai.expect;

// Disable the AJAX library used by the action creator
const noop = () => ( { mock: 'data' } );
mockery.enable( {
  warnOnReplace: false,
  warnOnUnregistered: false
} );
mockery.registerMock( 'xdr', noop );

const utils = require(
  BASE_JS_PATH + 'organisms/MortgagePerformanceTrends/utils.js'
);

let el;
const document = {
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

  it( 'should get metro data', () => {
    const cb = sinon.spy();
    expect( utils.getMetroData( cb ) ).to.deep.equal( { mock: 'data' } );
  } );

  it( 'should get non-metro data', () => {
    const cb = sinon.spy();
    expect( utils.getNonMetroData( cb ) ).to.deep.equal( { mock: 'data' } );
  } );

  it( 'should get county data', () => {
    const cb = sinon.spy();
    expect( utils.getCountyData( cb ) ).to.deep.equal( { mock: 'data' } );
  } );

  it( 'should get state data', () => {
    const cb = sinon.spy();
    expect( utils.getStateData( cb ) ).to.deep.equal( { mock: 'data' } );
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

  it( 'should be able to parse years in date strings', () => {
    expect( utils.getYear( '2008-01' ) ).to.equal( '2008' );
    expect( utils.getYear( '3099-01' ) ).to.equal( '3099' );
    expect( utils.getYear( '2012-01-01' ) ).to.equal( '2012' );
    expect( utils.getYear( 'blah' ) ).to.equal( 'blah' );
  } );

  it( 'should be able to parse months in date strings', () => {
    expect( utils.getMonth( '2008-01' ) ).to.equal( '01' );
    expect( utils.getMonth( '1999-11' ) ).to.equal( '11' );
    expect( utils.getMonth( '2012-05-01' ) ).to.equal( '05' );
    expect( utils.getMonth( 'blah' ) ).to.be.undefined;
  } );

  it( 'should be able to detect valid dates', () => {
    expect( utils.isDateValid( '2008-01', '2016-10-01' ) ).to.be.true;
    expect( utils.isDateValid( '2009-11', '2016-12-01' ) ).to.be.true;
    expect( utils.isDateValid( '2009-11', '2016-12' ) ).to.be.true;
    expect( utils.isDateValid( '2009-11-01', '2009-11-01' ) ).to.be.true;
    expect( utils.isDateValid( '2009-11-01', '2009-11' ) ).to.be.true;
    expect( utils.isDateValid( '2009-11', '2009-11' ) ).to.be.true;
    expect( utils.isDateValid( '2009-07', '2011-03' ) ).to.be.true;
  } );

  it( 'should be able to detect invalid dates', () => {
    expect( utils.isDateValid( '2017-01', '2014-10-01' ) ).to.be.false;
    expect( utils.isDateValid( 'foo', '2016-10-01' ) ).to.be.false;
    expect( utils.isDateValid( '2014-10', 'bar' ) ).to.be.false;
    expect( utils.isDateValid( 'foo', 'bar' ) ).to.be.false;
    expect( utils.isDateValid( '2011-01-01', '2010-10-01' ) ).to.be.false;
  } );

  it( 'should parse date strings', () => {
    let date = utils.getDate( '2009-01-01' );
    expect( date ).to.equal( 'January 2009' );
    date = utils.getDate( '2020-11-27' );
    expect( date ).to.equal( 'November 2020' );
    date = utils.getDate( 'cheeseburger' );
    expect( date ).to.equal( 'cheeseburger' );
  } );

  it( 'should parse counties\' states', () => {
    let state = utils.getCountyState( '01234' );
    expect( state ).to.equal( 'AL' );
    state = utils.getCountyState( '23502' );
    expect( state ).to.equal( 'ME' );
    state = utils.getCountyState( '30000' );
    expect( state ).to.equal( 'MT' );
    state = utils.getCountyState( '51412' );
    expect( state ).to.equal( 'VA' );
    state = utils.getCountyState( 'not a fips' );
    expect( state ).to.be.undefined;
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
