import { createRoute
} from '../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/models/route';
import routeOptionReducer, {
  addRouteOptionAction,
  clearAverageCostAction,
  clearDaysPerWeekAction,
  clearMilesAction,
  hasTodo,
  initialState,
  routeSelector,
  updateAverageCostAction,
  updateCostToActionPlan,
  updateDaysPerWeekAction,
  updateDaysToActionPlan,
  updateIsMonthlyCostAction,
  updateMilesAction,
  updateMilesToActionPlan,
  updateTimeToActionPlan,
  updateTransitTimeHoursAction,
  updateTransitTimeMinutesAction,
  updateTransportationAction
} from '../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/reducers/route-option-reducer';
import { UNDEFINED } from '../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/util';
import { PLAN_TYPES } from '../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/data-types/todo-items';

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
    const initialRoutes = routeOptionReducer(
      UNDEFINED, addRouteOptionAction( createRoute() )
    );
    const appState = {
      routes: initialRoutes
    };

    expect( typeof routeSelector === 'function' ).toBeTruthy();
    expect( routeSelector( appState.routes, 0 ) )
      .toEqual( initialRoutes.routes[0] );
    expect( routeSelector( appState.routes, 1 ) )
      .toStrictEqual( {} );

  } );

  it( 'exposes a helper to determine if a given plan type if in a route action plan', () => {
    const initialRoutes = routeOptionReducer(
      UNDEFINED, addRouteOptionAction( createRoute( {
        actionPlanItems: [ PLAN_TYPES.MILES ]
      } ) ) );
    const route = initialRoutes.routes[0];

    expect( hasTodo( route.actionPlanItems, PLAN_TYPES.MILES ) )
      .toBe( true );
    expect( hasTodo( route.actionPlanItems, PLAN_TYPES.AVERAGE_COST ) )
      .toBe( false );
  } );

  describe( 'updating a specific route', () => {
    let initial;

    beforeEach( () => {
      initial = routeOptionReducer(
        UNDEFINED, addRouteOptionAction( createRoute() )
      );
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
      Object.entries( rest ).forEach( ( [ key, value ] ) => expect( value )
        .toBe( initial.routes[0][key] )
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

      Object.entries( rest ).forEach( ( [ key, value ] ) => expect( value )
        .toBe( initial.routes[0][key] )
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

      Object.entries( rest ).forEach( ( [ key, value ] ) => expect( value )
        .toBe( initial.routes[0][key] )
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
      const { transitTimeHours, transitTimeMinutes } = state.routes[0];

      expect( transitTimeHours ).toBe( nextValue );
      expect( transitTimeMinutes ).toBe( '0' );

      const nextState = routeOptionReducer(
        {
          routes: [ createRoute( { transitTimeMinutes: '1' } ) ]
        },
        updateTransitTimeHoursAction( {
          routeIndex: 0,
          value: nextValue } )
      );

      expect( nextState.routes[0].transitTimeMinutes ).toBe( '1' );
    } );

    it( 'reduces the .updateTransitTimeMinutes action', () => {
      const state = routeOptionReducer(
        initial,
        updateTransitTimeMinutesAction( {
          routeIndex: 0,
          value: nextValue } )
      );
      const { transitTimeMinutes, transitTimeHours } = state.routes[0];

      expect( transitTimeMinutes ).toBe( nextValue );
      expect( transitTimeHours ).toBe( '0' );

      const nextState = routeOptionReducer(
        {
          routes: [ createRoute( { transitTimeHours: '1' } ) ]
        },
        updateTransitTimeMinutesAction( {
          routeIndex: 0,
          value: nextValue } )
      );

      expect( nextState.routes[0].transitTimeHours ).toBe( '1' );
    } );

    it( 'properly reduces the state of the actionPlanItems list', () => {
      const state = routeOptionReducer(
        {
          routes: [
            createRoute( {
              actionPlanItems: [ PLAN_TYPES.TIME, PLAN_TYPES.MILES ]
            } )
          ]
        },
        updateTimeToActionPlan( {
          routeIndex: 0,
          value: false } )
      );

      const todos = routeSelector( state, 0 ).actionPlanItems;

      expect( todos.length ).toBe( 1 );
      expect( todos[0] ).toBe( PLAN_TYPES.MILES );
    } );

    it( 'reduces the state of actionPlanItems when a mismatching type is supplied', () => {
      const state = routeOptionReducer(
        {
          routes: [
            createRoute( {
              actionPlanItems: [ PLAN_TYPES.TIME ]
            } )
          ]
        },
        updateMilesToActionPlan( {
          routeIndex: 0,
          value: false } )
      );

      const todos = routeSelector( state, 0 ).actionPlanItems;

      expect( todos.length ).toBe( 1 );
      expect( todos[0] ).toBe( PLAN_TYPES.TIME );
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

    it( 'reduces the .updateMilesToActionPlan action', () => {
      const state = routeOptionReducer(
        initial,
        updateMilesToActionPlan( {
          routeIndex: 0,
          value: true } )
      );

      const { actionPlanItems } = state.routes[0];

      expect( actionPlanItems.length ).toBe( 1 );
      expect( actionPlanItems[0] ).toBeDefined();
      expect( actionPlanItems[0] ).toBe( PLAN_TYPES.MILES );
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
        addRouteOptionAction( createRoute( route ) )
      );

      expect( state.routes[0].averageCost ).toBe( route.averageCost );
      expect( state.routes[0].isMonthlyCost ).toBe( route.isMonthlyCost );
      expect( state.routes[0].actionPlanItems ).toBe( route.actionPlanItems );
      expect( state.routes[0].actionPlanItems[0] ).toBeDefined();

      state = routeOptionReducer(
        state,
        clearAverageCostAction( { routeIndex: 0 } )
      );

      expect( state.routes[0].averageCost ).toBe( '' );
      expect( state.routes[0].isMonthlyCost ).toBe( null );
      expect( state.routes[0].actionPlanItems.length ).toBe( 0 );
    } );

    it( 'reduces the .clearDaysPerWeekAction', () => {
      const routeIndex = 0;
      const route = {
        daysPerWeek: '2',
        actionPlanItems: [ PLAN_TYPES.DAYS_PER_WEEK ]
      };
      let state = routeOptionReducer(
        UNDEFINED,
        addRouteOptionAction( createRoute( route ) )
      );

      let currRoute = routeSelector( state, routeIndex );

      expect( currRoute.daysPerWeek ).toBe( route.daysPerWeek );
      expect( currRoute.actionPlanItems ).toBe( route.actionPlanItems );
      expect( currRoute.actionPlanItems[0] ).toBeDefined();

      state = routeOptionReducer(
        state,
        clearDaysPerWeekAction( { routeIndex, value: false } )
      );

      currRoute = routeSelector( state, routeIndex );

      expect( currRoute.daysPerWeek ).toBe( '' );
      expect( currRoute.actionPlanItems.length ).toBe( 0 );
    } );

    it( 'reduces the .clearMilesAction', () => {
      const routeIndex = 0;
      const route = {
        miles: '25',
        actionPlanItems: [ PLAN_TYPES.MILES ]
      };
      let state = routeOptionReducer(
        UNDEFINED,
        addRouteOptionAction( route )
      );

      let currRoute = routeSelector( state, routeIndex );

      expect( currRoute.miles ).toBe( route.miles );
      expect( currRoute.actionPlanItems ).toBe( route.actionPlanItems );
      expect( currRoute.actionPlanItems[0] ).toBeDefined();

      state = routeOptionReducer(
        state,
        clearMilesAction( { routeIndex } )
      );

      currRoute = routeSelector( state, routeIndex );

      expect( currRoute.miles ).toBe( '' );
      expect( currRoute.actionPlanItems.length ).toBe( 0 );
    } );
  } );
} );
