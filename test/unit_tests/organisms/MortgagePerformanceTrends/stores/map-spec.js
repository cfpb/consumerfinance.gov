const BASE_JS_PATH = '../../../../../cfgov/unprocessed/js/';

const chai = require( 'chai' );
const expect = chai.expect;
const Store = require(
  BASE_JS_PATH + 'organisms/MortgagePerformanceTrends/stores/map.js'
);
let store;

describe( 'Mortgage Performance map store', () => {

  beforeEach( () => {
    store = new Store( {} );
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

  it( 'should properly clear geos', () => {
    const action = {
      type: 'CLEAR_GEO'
    };
    store.dispatch( action );
    expect( store.getState().geo.type ).to.equal( null );
    expect( store.getState().geo.id ).to.equal( null );
    expect( store.getState().geo.name ).to.equal( null );
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
    const action = {
      type: 'REQUEST_METROS'
    };
    store.dispatch( action );
    expect( store.getState().isLoadingMetros ).to.be.true;
  } );

  it( 'should properly reduce fetching metros', () => {
    const action = {
      type: 'FETCH_METROS'
    };
    store.dispatch( action );
    expect( store.getState().metros.length ).to.equal( 0 );
  } );

  it( 'should properly reduce fetching counties', () => {
    const action = {
      type: 'FETCH_COUNTIES'
    };
    store.dispatch( action );
    expect( store.getState().counties.length ).to.equal( 0 );
  } );

  it( 'should properly reduce loading counties state', () => {
    const action = {
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
    action = {
      type: 'UPDATE_CHART',
      geo: {
        type: 'metro',
        id: '67890',
        name: 'Boston, MA'
      },
      metros: { 67890: 'Boston, MA' }
    };
    store.dispatch( action );
    expect( store.getState().metros ).to.deep.equal( { 67890: 'Boston, MA' } );
  } );

  it( 'should properly reduce counties', () => {
    let action = {
      type: 'SET_COUNTIES',
      counties: { 12345: 'Acme County' }
    };
    store.dispatch( action );
    expect( store.getState().counties )
      .to.deep.equal( { 12345: 'Acme County' } );
    action = {
      type: 'UPDATE_CHART',
      geo: {
        type: 'county',
        id: '67890',
        name: 'Some other county'
      },
      counties: { 67890: 'Some other county' }
    };
    store.dispatch( action );
    expect( store.getState().counties )
      .to.deep.equal( { 67890: 'Some other county' } );
  } );

  it( 'should properly chart zooming', () => {
    const action = {
      type: 'ZOOM_CHART',
      target: 'MA'
    };
    store.dispatch( action );
    expect( store.getState().zoomTarget ).to.equal( 'MA' );
  } );

} );
