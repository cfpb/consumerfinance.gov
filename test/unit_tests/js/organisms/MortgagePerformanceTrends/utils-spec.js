// Disable the AJAX library used by the action creator.
jest.mock( 'xdr', () => jest.fn( () => ( { mock: 'data' } ) ) );

import
utils
  // eslint-disable-next-line max-len
  from '../../../../../cfgov/unprocessed/js/organisms/MortgagePerformanceTrends/utils.js';

let el;

describe( 'Mortgage Performance utilities', () => {

  beforeEach( () => {
    el = {
      style: {},
      disabled: false
    };
  } );

  it( 'should clear an element\'s diplay property', () => {
    utils.showEl( el );
    expect( el.style.display ).toBe( '' );
  } );

  it( 'should set an element\'s diplay property', () => {
    utils.hideEl( el );
    expect( el.style.display ).toBe( 'none' );
  } );

  it( 'should disable an element', () => {
    utils.disableEl( el );
    expect( el.disabled ).toBe( true );
  } );

  it( 'should un-disable an element', () => {
    utils.enableEl( el );
    expect( el.disabled ).toBe( false );
  } );

  it( 'should be able to create a select option', () => {
    const option = utils.addOption( {
      document,
      value: 'AL',
      text: 'Alabama',
      selected: false
    } );
    expect( option.value ).toBe( 'AL' );
    expect( option.text ).toBe( 'Alabama' );
  } );

  it( 'should get metro data', () => {
    const cb = jest.fn();
    expect( utils.getMetroData( cb ) ).toStrictEqual( { mock: 'data' } );
  } );

  it( 'should get non-metro data', () => {
    const cb = jest.fn();
    expect( utils.getNonMetroData( cb ) ).toStrictEqual( { mock: 'data' } );
  } );

  it( 'should get county data', () => {
    const cb = jest.fn();
    expect( utils.getCountyData( cb ) ).toStrictEqual( { mock: 'data' } );
  } );

  it( 'should get state data', () => {
    const cb = jest.fn();
    expect( utils.getStateData( cb ) ).toStrictEqual( { mock: 'data' } );
  } );

  it( 'should be able to calculate zoom levels', () => {
    // Not a pure function. The following behavior is expected.
    expect( utils.getZoomLevel( 5 ) ).toBe( 0.5 );
    expect( utils.getZoomLevel( 5 ) ).toBe( 1 );
  } );

  it( 'should be able to set zoom levels', () => {
    expect( utils.setZoomLevel( 5 ) ).toBe( 5 );
    expect( utils.setZoomLevel( 7 ) ).toBe( 7 );
    expect( utils.setZoomLevel( 234.56 ) ).toBe( 234.56 );
  } );

  it( 'should be able to parse years in date strings', () => {
    expect( utils.getYear( '2008-01' ) ).toBe( '2008' );
    expect( utils.getYear( '3099-01' ) ).toBe( '3099' );
    expect( utils.getYear( '2012-01-01' ) ).toBe( '2012' );
    expect( utils.getYear( 'blah' ) ).toBe( 'blah' );
  } );

  it( 'should be able to parse months in date strings', () => {
    expect( utils.getMonth( '2008-01' ) ).toBe( '01' );
    expect( utils.getMonth( '1999-11' ) ).toBe( '11' );
    expect( utils.getMonth( '2012-05-01' ) ).toBe( '05' );
    expect( utils.getMonth( 'blah' ) ).toBeUndefined();
  } );

  it( 'should be able to detect valid dates', () => {
    expect( utils.isDateValid( '2008-01', '2016-10-01' ) ).toBe( true );
    expect( utils.isDateValid( '2009-11', '2016-12-01' ) ).toBe( true );
    expect( utils.isDateValid( '2009-11', '2016-12' ) ).toBe( true );
    expect( utils.isDateValid( '2009-11-01', '2009-11-01' ) ).toBe( true );
    expect( utils.isDateValid( '2009-11-01', '2009-11' ) ).toBe( true );
    expect( utils.isDateValid( '2009-11', '2009-11' ) ).toBe( true );
    expect( utils.isDateValid( '2009-07', '2011-03' ) ).toBe( true );
  } );

  it( 'should be able to detect invalid dates', () => {
    expect( utils.isDateValid( '2017-01', '2014-10-01' ) ).toBe( false );
    expect( utils.isDateValid( 'foo', '2016-10-01' ) ).toBe( false );
    expect( utils.isDateValid( '2014-10', 'bar' ) ).toBe( false );
    expect( utils.isDateValid( 'foo', 'bar' ) ).toBe( false );
    expect( utils.isDateValid( '2011-01-01', '2010-10-01' ) ).toBe( false );
  } );

  it( 'should parse date strings', () => {
    let date = utils.getDate( '2009-01-01' );
    expect( date ).toBe( 'January 2009' );
    date = utils.getDate( '2020-11-27' );
    expect( date ).toBe( 'November 2020' );
    date = utils.getDate( 'cheeseburger' );
    expect( date ).toBe( 'cheeseburger' );
  } );

  it( 'should parse counties\' states', () => {
    let state = utils.getCountyState( '01234' );
    expect( state ).toBe( 'AL' );
    state = utils.getCountyState( '23502' );
    expect( state ).toBe( 'ME' );
    state = utils.getCountyState( '30000' );
    expect( state ).toBe( 'MT' );
    state = utils.getCountyState( '51412' );
    expect( state ).toBe( 'VA' );
    state = utils.getCountyState( 'not a fips' );
    expect( state ).toBeUndefined();
  } );

  it( 'check if a FIPS is a non-metro area', () => {
    let location = utils.isNonMetro( '87364' );
    expect( location ).toBe( false );
    location = utils.isNonMetro( '1234567890' );
    expect( location ).toBe( false );
    location = utils.isNonMetro( '06-non' );
    expect( location ).toBe( true );
    location = utils.isNonMetro( 'non-06' );
    expect( location ).toBe( false );
  } );

} );
