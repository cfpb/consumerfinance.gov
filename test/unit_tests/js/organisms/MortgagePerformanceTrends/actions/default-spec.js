/* Disable the AJAX library used by the action creator.
   Unfortunately, we can't place path variables into import statements. */
import
* as defaultActionCreators
  // eslint-disable-next-line max-len
  from '../../../../../../cfgov/unprocessed/js/organisms/MortgagePerformanceTrends/actions/default.js';
const actions = defaultActionCreators.default();

jest.mock( 'xdr', () => jest.fn( () => ( { mock: 'data' } ) ) );
jest.mock( '../../../../../../cfgov/unprocessed/js/organisms/' +
           'MortgagePerformanceTrends/utils', () => ( {
  getNonMetroData: cb => {
    const nonMetros = [ {
      valid: true,
      fips: '12345',
      name: 'Acme metro',
      abbr: 'AL'
    } ];
    cb( nonMetros );
  }
} ) );

describe( 'Mortgage Performance default action creators', () => {

  it( 'should create an action to set a geo', () => {
    const action = actions.setGeo( 12345, 'Alabama', 'state' );
    expect( action ).toStrictEqual( {
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
    expect( action ).toStrictEqual( {
      type: 'CLEAR_GEO'
    } );
  } );

  it( 'should create actions to update charts', () => {
    let action = actions.updateChart( 12345, 'Alabama', 'state', false );
    expect( action ).toStrictEqual( {
      type: 'UPDATE_CHART',
      geo: {
        type: 'state',
        id: 12345,
        name: 'Alabama'
      },
      includeComparison: false
    } );
    action = actions.updateChart( null, null, null, false );
    expect( action ).toStrictEqual( {
      type: 'UPDATE_CHART',
      geo: {
        id: null,
        name: null
      },
      includeComparison: false
    } );
  } );

  it( 'should create an action to update the national comparison', () => {
    const action = actions.updateNational( false );
    expect( action ).toStrictEqual( {
      type: 'UPDATE_CHART',
      includeComparison: false
    } );
  } );

  it( 'should create an action to update the date', () => {
    const action = actions.updateDate( '2010-01' );
    expect( action ).toStrictEqual( {
      type: 'UPDATE_DATE',
      date: '2010-01'
    } );
  } );

  it( 'should create an action to request counties', () => {
    const action = actions.requestCounties();
    expect( action ).toStrictEqual( {
      type: 'REQUEST_COUNTIES',
      isLoadingCounties: true
    } );
  } );

  it( 'should create an action to request metros', () => {
    const action = actions.requestMetros();
    expect( action ).toStrictEqual( {
      type: 'REQUEST_METROS',
      isLoadingMetros: true
    } );
  } );

  it( 'should create an action to request non-metros', () => {
    const action = actions.requestNonMetros();
    expect( action ).toStrictEqual( {
      type: 'REQUEST_NON_METROS',
      isLoadingNonMetros: true
    } );
  } );

  it( 'should dispatch actions to fetch non-metros', () => {
    const dispatch = jest.fn();
    actions.fetchNonMetros( 'AL', true )( dispatch );
    expect( dispatch ).toHaveBeenCalledTimes( 4 );
    actions.fetchNonMetros( 'CA', true )( dispatch );
    expect( dispatch ).toHaveBeenCalledTimes( 8 );
  } );

  it( 'should fail on bad non-metro state abbr', () => {
    expect( actions.fetchNonMetros( 'bloop', true ) ).toThrow();
  } );

  it( 'should create an action to set metros', () => {
    const action = actions.setMetros( [ { name: 'Akron, OH' } ] );
    expect( action ).toStrictEqual( {
      type: 'SET_METROS',
      metros: [ { name: 'Akron, OH' } ]
    } );
  } );

  it( 'should create an action to set non-metros', () => {
    const action = actions.setNonMetros( [ { name: 'Tampa, FL' } ] );
    expect( action ).toStrictEqual( {
      type: 'SET_NON_METROS',
      nonMetros: [ { name: 'Tampa, FL' } ]
    } );
  } );

  it( 'should create an action to set counties', () => {
    const action = actions.setCounties( [ { name: 'Acme County' } ] );
    expect( action ).toStrictEqual( {
      type: 'SET_COUNTIES',
      counties: [ { name: 'Acme County' } ]
    } );
  } );

  it( 'should create an action to start loading', () => {
    const action = actions.startLoading();
    expect( action ).toStrictEqual( {
      type: 'START_LOADING',
      isLoading: true
    } );
  } );

  it( 'should create an action to stop loading', () => {
    const action = actions.stopLoading();
    expect( action ).toStrictEqual( {
      type: 'STOP_LOADING',
      isLoading: false
    } );
  } );

} );
