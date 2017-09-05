'use strict';
const BASE_JS_PATH = '../../../../../cfgov/unprocessed/js/';

const chai = require( 'chai' );
const expect = chai.expect;
const Store = require( BASE_JS_PATH + 'organisms/MortgagePerformanceTrends/stores/map.js' );
let store;

describe( 'Mortgage Performance map store', () => {

  beforeEach( () => {
    store = new Store();
  } );

  it( 'should instantiate a store', () => {
    expect( store instanceof Store ).to.be.true;
  } );

  it( 'should inherit helper methods', () => {
    expect( store.getState() ).to.exist;
  } );

  it( 'should be able to add subscribers', () => {
    store.subscribe( () => true );
    expect( store.subscribers.length ).to.equal( 1 );
    store.subscribe( () => false );
    store.subscribe( () => 1 );
    expect( store.subscribers.length ).to.equal( 3 );
  } );

  it( 'should default to U.S. state geo', () => {
    expect( store.state.geo.type ).to.equal( 'state' );
    expect( store.state.geo.id ).to.equal( null );
    expect( store.state.geo.name ).to.equal( null );
  } );

  it( 'should default to having an empty previous state', () => {
    expect( store.prevState ).to.deep.equal( {} );
  } );

  it( 'should properly reduce geos', () => {
    const action = {
      type: 'SET_GEO',
      geo: {
        type: 'county',
        id: 12345,
        name: 'Acme County'
      }
    };
    store.dispatch( action );
    expect( store.getState().geo.type ).to.equal( 'county' );
    expect( store.getState().geo.id ).to.equal( 12345 );
    expect( store.getState().geo.name ).to.equal( 'Acme County' );
  } );

  it( 'should properly clear geos', () => {
    const action = {
      type: 'CLEAR_GEO'
    };
    store.dispatch( action );
    expect( store.getState().geo.type ).to.equal( null );
    expect( store.getState().geo.id ).to.equal( null );
    expect( store.getState().geo.name ).to.equal( null );
  } );

  it( 'should pass through geos if action is bad', () => {
    let action = {
      type: 'SET_GEO',
      geo: {
        type: 'county',
        id: 12345,
        name: 'Acme County'
      }
    };
    store.dispatch( action );
    action = {
      type: 'SOME_OTHER_ACTION'
    };
    store.dispatch( action );
    expect( store.getState().geo.type ).to.equal( 'county' );
    expect( store.getState().geo.id ).to.equal( 12345 );
    expect( store.getState().geo.name ).to.equal( 'Acme County' );
  } );

  it( 'should properly reduce app loading state', () => {
    let action = {
      type: 'REQUEST_DATA',
      isLoading: true
    };
    store.dispatch( action );
    expect( store.getState().isLoading ).to.be.true;
    action = {
      type: 'SOME_OTHER_ACTION'
    };
    store.dispatch( action );
    expect( store.getState().isLoading ).to.be.false;
  } );

  it( 'should properly reduce loading metros state', () => {
    let action = {
      type: 'REQUEST_METROS'
    };
    store.dispatch( action );
    expect( store.getState().isLoadingMetros ).to.be.true;
  } );

  it( 'should properly reduce loading counties state', () => {
    let action = {
      type: 'REQUEST_COUNTIES'
    };
    store.dispatch( action );
    expect( store.getState().isLoadingCounties ).to.be.true;
  } );

  it( 'should properly reduce metros', () => {
    let action = {
      type: 'SET_METROS',
      metros: { 12345: 'Akron, OH' }
    };
    store.dispatch( action );
    expect( store.getState().metros ).to.deep.equal( { 12345: 'Akron, OH' } );
  } );

  it( 'should properly reduce counties', () => {
    let action = {
      type: 'SET_COUNTIES',
      counties: { 12345: 'Acme County' }
    };
    store.dispatch( action );
    expect( store.getState().counties ).to.deep.equal( { 12345: 'Acme County' } );
  } );

} );
