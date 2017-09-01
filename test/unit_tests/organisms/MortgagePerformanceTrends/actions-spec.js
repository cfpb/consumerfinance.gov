'use strict';
const BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';

const chai = require( 'chai' );
const mockery = require('mockery');
const expect = chai.expect;

// Disable the AJAX library used by the action creator
const noop = () => ( {} );
mockery.enable({
  warnOnReplace: false,
  warnOnUnregistered: false
});
mockery.registerMock( 'xdr', noop );

const actions = require( BASE_JS_PATH + 'organisms/MortgagePerformanceTrends/actions.js' );

describe( 'Mortgage Performance action creator', () => {

  it( 'should create an action to set a geo', () => {
    const action = actions.setGeo( 12345, 'Alabama', 'state' );
    expect( action ).to.deep.equal( {
      type: 'SET_GEO',
      geo: {
        type: 'state',
        id: 12345,
        name: 'Alabama'
      }
    } );
  } );

  it( 'should create an action to clear geos', () => {
    const action = actions.clearGeo();
    expect( action ).to.deep.equal( {
      type: 'CLEAR_GEO'
    } );
  } );

  it( 'should create actions to update charts', () => {
    let action = actions.updateChart( 12345, 'Alabama', 'state', false );
    expect( action ).to.deep.equal( {
      type: 'UPDATE_CHART',
      geo: {
        type: 'state',
        id: 12345,
        name: 'Alabama'
      },
      includeNational: false
    } );
    action = actions.updateChart( null, null, null, false );
    expect( action ).to.deep.equal( {
      type: 'UPDATE_CHART',
      geo: {
        id: null,
        name: null
      },
      includeNational: false
    } );
  } );

  it( 'should create an action to update the national comparison', () => {
    const action = actions.updateNational( false );
    expect( action ).to.deep.equal( {
      type: 'UPDATE_CHART',
      includeNational: false
    } );
  } );

  it( 'should create an action to update the date', () => {
    const action = actions.updateDate( '2010-01' );
    expect( action ).to.deep.equal( {
      type: 'UPDATE_DATE',
      date: '2010-01'
    } );
  } );

  it( 'should create an action to request counties', () => {
    const action = actions.requestCounties();
    expect( action ).to.deep.equal( {
      type: 'REQUEST_COUNTIES',
      isLoadingCounties: true
    } );
  } );

  it( 'should create an action to request metros', () => {
    const action = actions.requestMetros();
    expect( action ).to.deep.equal( {
      type: 'REQUEST_METROS',
      isLoadingMetros: true
    } );
  } );

  it( 'should create an action to set metros', () => {
    const action = actions.setMetros( [ { name: 'Akron, OH' } ] );
    expect( action ).to.deep.equal( {
      type: 'SET_METROS',
      metros: [ { name: 'Akron, OH' } ]
    } );
  } );

  it( 'should create an action to set counties', () => {
    const action = actions.setCounties( [ { name: 'Acme County' } ] );
    expect( action ).to.deep.equal( {
      type: 'SET_COUNTIES',
      counties: [ { name: 'Acme County' } ]
    } );
  } );

  it( 'should create an action to start loading', () => {
    const action = actions.startLoading();
    expect( action ).to.deep.equal( {
      type: 'START_LOADING',
      isLoading: true
    } );
  } );

  it( 'should create an action to stop loading', () => {
    const action = actions.stopLoading();
    expect( action ).to.deep.equal( {
      type: 'STOP_LOADING',
      isLoading: false
    } );
  } );

} );
