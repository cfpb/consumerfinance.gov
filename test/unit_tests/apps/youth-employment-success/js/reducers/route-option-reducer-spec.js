import createRoute from '../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/route';
import routeOptionReducer, {
  addRouteOptionAction,
  initialState,
  routeSelector,
  updateDailyCostAction,
  updateDaysPerWeekAction,
  updateMilesAction,
  updateTransportationAction
} from '../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/reducers/route-option-reducer';
import { UNDEFINED } from '../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/util';

// Arbitrary value to ensure reducer is updating properly
const nextValue = '15';

describe( 'routeOptionReducer', () => {
  it( 'returns an initial state when it recevives an unsupported action type', () => {
    const state = routeOptionReducer( UNDEFINED, { type: null } );

    expect( state ).toEqual( initialState );
  } );

  it( 'reduces .addRouteOptionAction', () => {
    const state = routeOptionReducer( UNDEFINED, addRouteOptionAction( {} ) );

    expect( state.routes.length ).toBe( 1 );
  } );

  it( 'does not reduce routes for which it did not receive an index', () => {
    const transportationType = 'Walk';
    const state = routeOptionReducer( {
      routes: [ createRoute(), createRoute() ]
    },
    updateTransportationAction( { routeIndex: 0, value: transportationType } )
    );

    expect( state.routes[0].transportation ).toBe( transportationType );
    expect( state.routes[1].transportation ).toBe( '' );
  } );

  it( 'exposes a selector to decouple data from reducer shape', () => {
    const state = routeOptionReducer( {
      routes: [ createRoute(), createRoute( { transportation: 'Walk' } ) ]
    },
    { type: null }
    );

    expect( routeSelector( state, 1 ).transportation ).toBe( 'Walk' );
  } );

  describe( 'updating a specific route', () => {
    let initial;

    beforeEach( () => {
      initial = routeOptionReducer( UNDEFINED, addRouteOptionAction( {} ) );
    } );

    it( 'reduces .updateDailyCostAction', () => {
      const state = routeOptionReducer(
        initial,
        updateDailyCostAction( {
          routeIndex: 0,
          value: nextValue
        } )
      );
      const { dailyCost, ...rest } = state.routes[0];

      expect( dailyCost ).toBe( nextValue );
      Object.entries( rest ).forEach( ( [ key, value ] ) => expect( value ).toBe( initialState[key] )
      );
    } );

    it( 'reduces .updateDaysPerWeekAction', () => {
      const state = routeOptionReducer(
        initial,
        updateDaysPerWeekAction( {
          routeIndex: 0,
          value: nextValue } )
      );
      const { daysPerWeek, ...rest } = state.routes[0];

      expect( daysPerWeek ).toBe( nextValue );
      Object.entries( rest ).forEach( ( [ key, value ] ) => expect( value ).toBe( initialState[key] )
      );
    } );

    it( 'reduces .updateMilesAction', () => {
      const state = routeOptionReducer(
        initial,
        updateMilesAction( {
          routeIndex: 0,
          value: nextValue } )
      );
      const { miles, ...rest } = state.routes[0];
      expect( miles ).toBe( nextValue );
      Object.entries( rest ).forEach( ( [ key, value ] ) => expect( value ).toBe( initialState[key] )
      );
    } );

    it( 'reduces .updateTransportation', () => {
      let state = routeOptionReducer(
        initial,
        updateTransportationAction( {
          routeIndex: 0,
          value: 'Walk' } )
      );

      let route = state.routes[0];
      expect( route.transportation ).toBe( 'Walk' );

      state = routeOptionReducer(
        state,
        updateTransportationAction( {
          routeIndex: 0,
          value: 'Drive' } )
      );

      route = state.routes[0];
      expect( route.transportation ).toBe( 'Drive' );
    } );
  } );
} );
