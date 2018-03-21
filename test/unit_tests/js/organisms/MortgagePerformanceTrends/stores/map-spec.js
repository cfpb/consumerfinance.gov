const BASE_JS_PATH = '../../../../../../cfgov/unprocessed/js/';
const Store = require(
  BASE_JS_PATH + 'organisms/MortgagePerformanceTrends/stores/map.js'
);
let store;

describe( 'Mortgage Performance map store', () => {

  beforeEach( () => {
    store = new Store( {} );
  } );

  it( 'should instantiate a store', () => {
    expect( store instanceof Store ).toBe( true );
  } );

  it( 'should inherit helper methods', () => {
    const mockData = {
      geo: { type: 'state', id: null, name: null },
      isLoadingMetros: false,
      isLoadingCounties: false,
      isLoading: false,
      zoomTarget: null,
      counties: [],
      metros: []
    };

    expect( store.getState() ).toEqual( mockData );
  } );

  it( 'should be able to add subscribers', () => {
    store.subscribe( () => true );
    expect( store.subscribers.length ).toBe( 1 );
    store.subscribe( () => false );
    store.subscribe( () => 1 );
    expect( store.subscribers.length ).toBe( 3 );
  } );

  it( 'should default to U.S. state geo', () => {
    expect( store.state.geo.type ).toBe( 'state' );
    expect( store.state.geo.id ).toBeNull();
    expect( store.state.geo.name ).toBeNull();
  } );

  it( 'should default to having an empty previous state', () => {
    expect( store.prevState ).toEqual( {} );
  } );

  it( 'should properly clear geos', () => {
    const action = {
      type: 'CLEAR_GEO'
    };
    store.dispatch( action );
    expect( store.getState().geo.type ).toBeNull();
    expect( store.getState().geo.id ).toBeNull();
    expect( store.getState().geo.name ).toBeNull();
  } );

  it( 'should properly reduce app loading state', () => {
    let action = {
      type: 'REQUEST_DATA',
      isLoading: true
    };
    store.dispatch( action );
    expect( store.getState().isLoading ).toBe( true );
    action = {
      type: 'SOME_OTHER_ACTION'
    };
    store.dispatch( action );
    expect( store.getState().isLoading ).toBe( false );
  } );

  it( 'should properly reduce loading metros state', () => {
    const action = {
      type: 'REQUEST_METROS'
    };
    store.dispatch( action );
    expect( store.getState().isLoadingMetros ).toBe( true );
  } );

  it( 'should properly reduce fetching metros', () => {
    const action = {
      type: 'FETCH_METROS'
    };
    store.dispatch( action );
    expect( store.getState().metros.length ).toBe( 0 );
  } );

  it( 'should properly reduce fetching counties', () => {
    const action = {
      type: 'FETCH_COUNTIES'
    };
    store.dispatch( action );
    expect( store.getState().counties.length ).toBe( 0 );
  } );

  it( 'should properly reduce loading counties state', () => {
    const action = {
      type: 'REQUEST_COUNTIES'
    };
    store.dispatch( action );
    expect( store.getState().isLoadingCounties ).toBe( true );
  } );

  it( 'should properly reduce metros', () => {
    let action = {
      type: 'SET_METROS',
      metros: { 12345: 'Akron, OH' }
    };
    store.dispatch( action );
    expect( store.getState().metros ).toEqual( { 12345: 'Akron, OH' } );
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
    expect( store.getState().metros ).toEqual( { 67890: 'Boston, MA' } );
  } );

  it( 'should properly reduce counties', () => {
    let action = {
      type: 'SET_COUNTIES',
      counties: { 12345: 'Acme County' }
    };
    store.dispatch( action );
    expect( store.getState().counties ).toEqual( { 12345: 'Acme County' } );
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
      .toEqual( { 67890: 'Some other county' } );
  } );

  it( 'should properly chart zooming', () => {
    const action = {
      type: 'ZOOM_CHART',
      target: 'MA'
    };
    store.dispatch( action );
    expect( store.getState().zoomTarget ).toBe( 'MA' );
  } );

} );
