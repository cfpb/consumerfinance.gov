import { actionCreator, assign } from '../util';
import { PLAN_TYPES } from '../data/todo-items';

const initialState = {
  routes: []
};

const actionTypes = Object.freeze( {
  ADD_ROUTE_OPTION: 'ADD_ROUTE_OPTION',
  UPDATE_TRANSPORTATION: 'UPDATE_TRANSPORTATION',
  UPDATE_MILES: 'UPDATE_MILES',
  UPDATE_AVERAGE_COST: 'UPDATE_AVERAGE_COST',
  UPDATE_DAYS_PER_WEEK: 'UPDATE_DAYS_PER_WEEK',
  UPDATE_TIME_TO_ACTION_PLAN: 'UPDATE_TIME_TO_ACTION_PLAN',
  UPDATE_TRANSIT_TIME_HOURS: 'UPDATE_TRANSIT_TIME_HOURS',
  UPDATE_TRANSIT_TIME_MINUTES: 'UPDATE_TRANSIT_TIME_MINUTES'
} );

const addRouteOptionAction = actionCreator(
  actionTypes.ADD_ROUTE_OPTION
);
const updateTransportationAction = actionCreator(
  actionTypes.UPDATE_TRANSPORTATION
);
const updateMilesAction = actionCreator(
  actionTypes.UPDATE_MILES
);
const updateDaysPerWeekAction = actionCreator(
  actionTypes.UPDATE_DAYS_PER_WEEK
);
const updateAverageCostAction = actionCreator(
  actionTypes.UPDATE_AVERAGE_COST
);
const updateTimeToActionPlan = actionCreator(
  actionTypes.UPDATE_TIME_TO_ACTION_PLAN
);
const updateTransitTimeHoursAction = actionCreator(
  actionTypes.UPDATE_TRANSIT_TIME_HOURS
);
const updateTransitTimeMinutesAction = actionCreator(
  actionTypes.UPDATE_TRANSIT_TIME_MINUTES
);

/**
 *
 * @param {object} state the current state of this reducer
 * @param {number} index the index of the route we want to retrieve
 * @returns {object} the route object at the desired index
 */
function routeSelector( state, index ) {
  return state.routes[index] || {};
}

/**
 *
 * @param {array} routes Route options the user has created
 * @param {object} nextRoute a route model object
 * @returns {array} the array of routes with the most recent route added
 */
function addRouteOption( routes, nextRoute ) {
  return routes.concat( nextRoute );
}

/**
 * Helper function to add / remove a plan item
 * @param {array} actionPlan The plan item types currently in the user's action plan
 * @param {string} itemType The plan item type to add or remove
 * @param {boolean} doUpdate How the plan should be amended
 *
 * @returns {Array} The new action plan
 */
function updateActionPlan( actionPlan, itemType, doUpdate ) {
  if ( !doUpdate ) {
    actionPlan.splice( actionPlan.indexOf( itemType ) );

    return actionPlan.slice();
  }

  return actionPlan.concat( PLAN_TYPES.TIME );
}

/**
 *
 * @param {array} routes the array of routes in the reducer's state
 * @param {number} routeIndex the index of the route object we want to update
 * @param {object} data object describing the updates we want to make
 *  to the route object's proeprties
 * @returns {object} the next state of the reducer
 */
function updateRouteData( routes, routeIndex, data ) {
  const computedState = {
    routes: routes.map( ( route, index ) => {
      if ( index !== routeIndex ) {
        return route;
      }

      return assign( route, data );
    } )
  };

  return computedState;
}

/**
 *
 * @param {object} state the current values for this slice of app state
 * @param {object} action instructs reducer which state update to apply
 * @returns {object} the updated state object
 */
function routeOptionReducer( state = initialState, action ) {
  const { type, data } = action;

  switch ( type ) {
    case actionTypes.ADD_ROUTE_OPTION: {
      return assign( state, {
        routes: addRouteOption( state.routes, data )
      } );
    }
    case actionTypes.UPDATE_AVERAGE_COST: {
      return assign( state, updateRouteData(
        state.routes,
        data.routeIndex,
        { averageCost: data.value } )
      );
    }
    case actionTypes.UPDATE_DAYS_PER_WEEK: {
      return assign( state, updateRouteData( state.routes, data.routeIndex, {
        daysPerWeek: data.value
      } ) );
    }
    case actionTypes.UPDATE_MILES: {
      return assign( state, updateRouteData( state.routes, data.routeIndex, {
        miles: data.value
      } ) );
    }
    case actionTypes.UPDATE_TRANSPORTATION: {
      return assign( state, updateRouteData( state.routes, data.routeIndex, {
        transportation: data.value
      } )
      );
    }
    case actionTypes.UPDATE_TIME_TO_ACTION_PLAN: {
      const index = action.data.routeIndex;
      const previousPlanItems = state.routes[index].actionPlanItems;
      const nextPlanItems = updateActionPlan(
        previousPlanItems,
        PLAN_TYPES.TIME,
        data.value
      );

      return assign( state, updateRouteData( state.routes, data.routeIndex, {
        actionPlanItems: nextPlanItems
      } ) );
    }
    case actionTypes.UPDATE_TRANSIT_TIME_HOURS: {
      return assign( state, updateRouteData( state.routes, data.routeIndex, {
        transitTimeHours: data.value
      } ) );
    }
    case actionTypes.UPDATE_TRANSIT_TIME_MINUTES: {
      return assign( state, updateRouteData( state.routes, data.routeIndex, {
        transitTimeMinutes: data.value
      } ) );
    }
    default:
      return state;
  }
}

export {
  initialState,
  addRouteOptionAction,
  routeSelector,
  updateTransportationAction,
  updateMilesAction,
  updateDaysPerWeekAction,
  updateAverageCostAction,
  updateTimeToActionPlan,
  updateTransitTimeHoursAction,
  updateTransitTimeMinutesAction
};

export default routeOptionReducer;
