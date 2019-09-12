import createRoute from '../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/route';
import routeOptionReducer, {
  addRouteOptionAction,
  clearAverageCostAction,
  initialState,
  routeSelector,
  updateAverageCostAction,
  updateCostToActionPlan,
  updateDaysPerWeekAction,
  updateIsMonthlyCostAction,
  updateMilesAction,
  updateTimeToActionPlan,
  updateTransitTimeHoursAction,
  updateTransitTimeMinutesAction,
  updateTransportationAction,
  updateDaysToActionPlan
} from '../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/reducers/route-option-reducer';
import { UNDEFINED } from '../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/util';
import { PLAN_TYPES } from '../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/data/todo-items';

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

  it( 'exposes a selector to decouple state form state shape', () => {
    const initialRoutes = routeOptionReducer( UNDEFINED, addRouteOptionAction( createRoute() ) );
    const appState = {
      routes: initialRoutes
    };

    expect( typeof routeSelector === 'function' ).toBeTruthy();
    expect( routeSelector( appState.routes, 0 ) ).toEqual( initialRoutes.routes[0] );
    expect( routeSelector( appState.routes, 1 ) ).toStrictEqual( {} );

  } );

  describe( 'updating a specific route', () => {
    let initial;

    beforeEach( () => {
      initial = routeOptionReducer( UNDEFINED, addRouteOptionAction( createRoute() ) );
    } );

    it( 'reduces .updateAverageCostAction', () => {
      const state = routeOptionReducer(
        initial,
        updateAverageCostAction( {
          routeIndex: 0,
          value: nextValue
        } )
      );
      const { averageCost, ...rest } = state.routes[0];

      expect( averageCost ).toBe( nextValue );
      Object.entries( rest ).forEach( ( [ key, value ] ) => expect( value ).toBe( initial.routes[0][key] )
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

      Object.entries( rest ).forEach( ( [ key, value ] ) => expect( value ).toBe( initial.routes[0][key] )
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

      Object.entries( rest ).forEach( ( [ key, value ] ) => expect( value ).toBe( initial.routes[0][key] )
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

    it( 'reduces the .updateTransitTimeHours action', () => {
      const state = routeOptionReducer(
        initial,
        updateTransitTimeHoursAction( {
          routeIndex: 0,
          value: nextValue } )
      );
      const { transitTimeHours } = state.routes[0];

      expect( transitTimeHours ).toBe( nextValue );
    } );

    it( 'reduces the .updateTransitTimeMinutes action', () => {
      const state = routeOptionReducer(
        initial,
        updateTransitTimeMinutesAction( {
          routeIndex: 0,
          value: nextValue } )
      );
      const { transitTimeMinutes } = state.routes[0];

      expect( transitTimeMinutes ).toBe( nextValue );
    } );

    it( 'reduces the .updateTimeToActionPlan action', () => {
      const state = routeOptionReducer(
        initial,
        updateTimeToActionPlan( {
          routeIndex: 0,
          value: true } )
      );

      const { actionPlanItems } = state.routes[0];

      expect( actionPlanItems.length ).toBe( 1 );
      expect( actionPlanItems[0] ).toBeDefined();
      expect( actionPlanItems[0] ).toBe( PLAN_TYPES.TIME );
    } );

    it( 'reduces the .updateCostToActionPlan action', () => {
      const state = routeOptionReducer(
        initial,
        updateCostToActionPlan( {
          routeIndex: 0,
          value: true } )
      );

      const { actionPlanItems } = state.routes[0];

      expect( actionPlanItems.length ).toBe( 1 );
      expect( actionPlanItems[0] ).toBeDefined();
      expect( actionPlanItems[0] ).toBe( PLAN_TYPES.AVERAGE_COST );
    } );

    it( 'reduces the .updateDaysToActionPlan action', () => {
      const state = routeOptionReducer(
        initial,
        updateDaysToActionPlan( {
          routeIndex: 0,
          value: true } )
      );

      const { actionPlanItems } = state.routes[0];

      expect( actionPlanItems.length ).toBe( 1 );
      expect( actionPlanItems[0] ).toBeDefined();
      expect( actionPlanItems[0] ).toBe( PLAN_TYPES.DAYS_PER_WEEK );
    } );

    it( 'reduces the .updateIsMonthlyCostAction', () => {
      expect( initial.routes[0].isMonthlyCost ).toBe( null );

      let state = routeOptionReducer(
        initial,
        updateIsMonthlyCostAction( {
          routeIndex: 0,
          value: true } )
      );

      let { isMonthlyCost } = state.routes[0];

      expect( isMonthlyCost ).toBe( true );

      state = routeOptionReducer(
        initial,
        updateIsMonthlyCostAction( {
          routeIndex: 0,
          value: false } )
      );

      isMonthlyCost = state.routes[0].isMonthlyCost;

      expect( isMonthlyCost ).toBe( false );
    } );

    it( 'reduces non-boolean values into boolean ones', () => {
      const state = routeOptionReducer(
        initial,
        updateIsMonthlyCostAction( {
          routeIndex: 0,
          value: 'string' } )
      );

      const { isMonthlyCost } = state.routes[0];

      expect( isMonthlyCost ).toBe( true );
    } );

    it( 'reduces the .clearAverageCostAction', () => {
      const route = {
        averageCost: '100',
        isMonthlyCost: true,
        actionPlanItems: [ PLAN_TYPES.AVERAGE_COST ]
      };
      let state = routeOptionReducer(
        UNDEFINED,
        addRouteOptionAction( createRoute(route) )
      );

      expect( state.routes[0].averageCost ).toBe( route.averageCost );
      expect( state.routes[0].isMonthlyCost ).toBe( route.isMonthlyCost );
      expect( state.routes[0].actionPlanItems ).toBe( route.actionPlanItems );

      state = routeOptionReducer(
        state,
        clearAverageCostAction( { routeIndex: 0 } )
      );

      expect( state.routes[0].averageCost ).toBe( '' );
      expect( state.routes[0].isMonthlyCost ).toBe( null );
      expect( state.routes[0].actionPlanItems.length ).toBe( 0 );
    } );
  } );
} );
