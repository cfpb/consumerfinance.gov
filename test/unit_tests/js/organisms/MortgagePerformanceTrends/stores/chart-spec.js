import
Store
  from '../../../../../../cfgov/unprocessed/js/organisms/MortgagePerformanceTrends/stores/chart.js';
let store;

describe( 'Mortgage Performance line chart store', () => {

  beforeEach( () => {
    store = new Store();
  } );

  it( 'should instantiate a store', () => {
    expect( store instanceof Store ).toBe( true );
  } );

  it( 'should inherit helper methods', () => {
    const mockData = {
      geo: { type: null, id: null, name: null },
      isLoading: false,
      isLoadingMetros: false,
      isLoadingNonMetros: false,
      isLoadingCounties: false,
      isLoadingStates: false,
      includeComparison: true,
      counties: {},
      metros: {},
      nonMetros: {},
      states: {}
    };

    expect( store.getState() ).toStrictEqual( mockData );
  } );

  it( 'should be able to add subscribers', () => {
    store.subscribe( () => true );
    expect( store.subscribers.length ).toBe( 1 );
  } );

  it( 'should default to no geo', () => {
    expect( store.state.geo.type ).toBeNull();
    expect( store.state.geo.id ).toBeNull();
    expect( store.state.geo.name ).toBeNull();
  } );

  it( 'should default to having an empty previous state', () => {
    expect( store.prevState ).toStrictEqual( {} );
  } );

  it( 'should default to comparing national data', () => {
    expect( store.state.includeComparison ).toBe( true );
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
    expect( store.getState().geo.type ).toStrictEqual( 'county' );
    expect( store.getState().geo.id ).toStrictEqual( 12345 );
    expect( store.getState().geo.name ).toStrictEqual( 'Acme County' );
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
    expect( store.getState().geo.type ).toBe( 'county' );
    expect( store.getState().geo.id ).toBe( 12345 );
    expect( store.getState().geo.name ).toBe( 'Acme County' );
  } );

  it( 'should properly reduce app loading state', () => {
    let action = {
      type: 'SET_GEO'
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

  it( 'should properly reduce loading non-metros state', () => {
    const action = {
      type: 'REQUEST_NON_METROS'
    };
    store.dispatch( action );
    expect( store.getState().isLoadingNonMetros ).toBe( true );
  } );

  it( 'should properly reduce loading counties state', () => {
    const action = {
      type: 'REQUEST_COUNTIES'
    };
    store.dispatch( action );
    expect( store.getState().isLoadingCounties ).toBe( true );
  } );

  it( 'should properly reduce loading u.s. states', () => {
    const action = {
      type: 'REQUEST_STATES'
    };
    store.dispatch( action );
    expect( store.getState().isLoadingStates ).toBe( true );
  } );

  it( 'should properly reduce metros', () => {
    const action = {
      type: 'SET_METROS',
      metros: { 12345: 'Akron, OH' }
    };
    store.dispatch( action );
    expect( store.getState().metros )
      .toStrictEqual( { 12345: 'Akron, OH' } );
  } );

  it( 'should properly reduce non-metros', () => {
    const action = {
      type: 'SET_NON_METROS',
      nonMetros: { 67890: 'Boston, MA' }
    };
    store.dispatch( action );
    expect( store.getState().nonMetros )
      .toStrictEqual( { 67890: 'Boston, MA' } );
  } );

  it( 'should properly reduce counties', () => {
    const action = {
      type: 'SET_COUNTIES',
      counties: { 12345: 'Acme County' }
    };
    store.dispatch( action );
    expect( store.getState().counties )
      .toStrictEqual( { 12345: 'Acme County' } );
  } );

  it( 'should properly reduce u.s. states', () => {
    let action = {
      type: 'SET_STATES',
      states: { AL: 'Alabama' }
    };
    store.dispatch( action );
    expect( store.getState().states ).toStrictEqual( { AL: 'Alabama' } );
    action = {
      type: 'FETCH_STATES',
      states: { CA: 'California' }
    };
    store.dispatch( action );
    expect( store.getState().states ).toStrictEqual( { AL: 'Alabama' } );
    action = {
      type: 'SET_STATES',
      states: { CA: 'California' }
    };
    store.dispatch( action );
    expect( store.getState().states ).toStrictEqual( { CA: 'California' } );
  } );

  it( 'should properly reduce national comparison', () => {
    let action = {
      type: 'UPDATE_CHART'
    };
    store.dispatch( action );
    expect( store.getState().includeComparison ).toBe( true );
    action = {
      type: 'UPDATE_CHART',
      includeComparison: false
    };
    store.dispatch( action );
    expect( store.getState().includeComparison ).toBe( false );
  } );

} );
