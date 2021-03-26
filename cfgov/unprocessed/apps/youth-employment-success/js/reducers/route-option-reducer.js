import { actionCreator, assign } from '../util';
import { PLAN_TYPES } from '../data-types/todo-items';

const initialState = {
  routes: []
};

const actionTypes = Object.freeze( {
  ADD_ROUTE_OPTION: 'ADD_ROUTE_OPTION',
  CLEAR_AVERAGE_COST: 'CLEAR_AVERAGE_COST',
  CLEAR_DAYS_PER_WEEK: 'CLEAR_DAYS_PER_WEEK',
  CLEAR_MILES: 'CLEAR_MILES',
  UPDATE_TRANSPORTATION: 'UPDATE_TRANSPORTATION',
  UPDATE_MILES: 'UPDATE_MILES',
  UPDATE_AVERAGE_COST: 'UPDATE_AVERAGE_COST',
  UPDATE_IS_MONTHLY_COST: 'UPDATE_IS_MONTHLY_COST',
  UPDATE_DAYS_PER_WEEK: 'UPDATE_DAYS_PER_WEEK',
  UPDATE_DAYS_TO_ACTION_PLAN: 'UPDATE_DAYS_TO_ACTION_PLAN',
  UPDATE_COST_TO_ACTION_PLAN: 'UPDATE_COST_TO_ACTION_PLAN',
  UPDATE_MILES_TO_ACTION_PLAN: 'UPDATE_MILES_TO_ACTION_PLAN',
  UPDATE_TIME_TO_ACTION_PLAN: 'UPDATE_TIME_TO_ACTION_PLAN',
  UPDATE_TRANSIT_TIME_HOURS: 'UPDATE_TRANSIT_TIME_HOURS',
  UPDATE_TRANSIT_TIME_MINUTES: 'UPDATE_TRANSIT_TIME_MINUTES'
} );

const addRouteOptionAction = actionCreator(
  actionTypes.ADD_ROUTE_OPTION
);
const clearAverageCostAction = actionCreator(
  actionTypes.CLEAR_AVERAGE_COST
);
const clearDaysPerWeekAction = actionCreator(
  actionTypes.CLEAR_DAYS_PER_WEEK
);
const clearMilesAction = actionCreator(
  actionTypes.CLEAR_MILES
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
const updateCostToActionPlan = actionCreator(
  actionTypes.UPDATE_COST_TO_ACTION_PLAN
);
const updateDaysToActionPlan = actionCreator(
  actionTypes.UPDATE_DAYS_TO_ACTION_PLAN
);
const updateTimeToActionPlan = actionCreator(
  actionTypes.UPDATE_TIME_TO_ACTION_PLAN
);
const updateMilesToActionPlan = actionCreator(
  actionTypes.UPDATE_MILES_TO_ACTION_PLAN
);
const updateTransitTimeHoursAction = actionCreator(
  actionTypes.UPDATE_TRANSIT_TIME_HOURS
);
const updateTransitTimeMinutesAction = actionCreator(
  actionTypes.UPDATE_TRANSIT_TIME_MINUTES
);
const updateIsMonthlyCostAction = actionCreator(
  actionTypes.UPDATE_IS_MONTHLY_COST
);

/**
 *
 * @param {object} state The current state of this reducer.
 * @param {number} index The index of the route we want to retrieve.
 * @returns {object} The route object at the indicated index.
 */
function routeSelector( state, index ) {
  return state.routes[index] || {};
}

/**
 *
 * @param {object} state The current state of this reducer.
 * @param {number} index The index of the route we want to retrieve.
 * @returns {Array} The todo list of actions the user needs to take for
 * the route at the indicated index.
 */
function todoListSelector( state, index ) {
  const route = routeSelector( state, index );

  return route.actionPlanItems || [];
}

/**
 * Predicate function to determine if a to-do list item is present in the
 * user's todo list of action items
 * @param {array} todoList The list of the user's current todos.
 * @param {string} todoType The type of plan item to test for.
 * @returns {Boolean} Whether or not the plan item is in the user's action plan.
 */
function hasTodo( todoList, todoType ) {
  return todoList.indexOf( todoType ) !== -1;
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
 * @param {object} state The application state.
 * @param {number} routeIndex The index of the route we want to target.
 * @param {string} itemType The plan item type to add or remove
 * @param {boolean} doUpdate How the plan should be amended
 *
 * @returns {Array} The new action plan
 */
function updateActionPlan( state, routeIndex, itemType, doUpdate ) {
  const actionPlan = todoListSelector( state, routeIndex );

  if ( !doUpdate ) {
    const toRemove = actionPlan.indexOf( itemType );

    if ( toRemove !== -1 ) {
      actionPlan.splice( toRemove, 1 );
    }

    return actionPlan.slice();
  }

  return actionPlan.concat( PLAN_TYPES[itemType] );
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
 * Detect if application should update the `transitTimeMinutes` state value
 * @param {Object} routes the routes state object
 * @param {Object} data The action's data
 * @param {Number} data.routeIndex The index of the route being updated
 * @returns {Boolean} Whether or not transitTimeMinutes is blank
 */
function hasTransitTimeMinutes( routes, data ) {
  const route = routeSelector( routes, data.routeIndex );

  if ( route.transitTimeMinutes === '' ) {
    return false;
  }

  return true;
}

/**
 * Detect if application should update the `transitTimeHours` state value
 * @param {Object} routes the routes state object
 * @param {Object} data The action's data
 * @param {Number} data.routeIndex The index of the route being updated
 * @returns {Boolean} Whether or not transitTimeHours is blank
 */
function hasTransitTimeHours( routes, data ) {
  const route = routeSelector( routes, data.routeIndex );

  if ( route.transitTimeHours === '' ) {
    return false;
  }

  return true;
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
    case actionTypes.CLEAR_AVERAGE_COST: {
      return assign( state, updateRouteData(
        state.routes,
        data.routeIndex,
        {
          averageCost: '',
          isMonthlyCost: null,
          actionPlanItems: updateActionPlan(
            state,
            action.data.routeIndex,
            PLAN_TYPES.AVERAGE_COST,
            false
          )
        }
      ) );
    }
    case actionTypes.CLEAR_DAYS_PER_WEEK: {
      return assign( state, updateRouteData(
        state.routes,
        action.data.routeIndex,
        {
          daysPerWeek: '',
          actionPlanItems: updateActionPlan(
            state,
            action.data.routeIndex,
            PLAN_TYPES.DAYS_PER_WEEK,
            false
          )
        }
      ) );
    }
    case actionTypes.CLEAR_MILES: {
      return assign( state, updateRouteData(
        state.routes,
        data.routeIndex,
        {
          miles: '',
          actionPlanItems: updateActionPlan(
            state,
            action.data.routeIndex,
            PLAN_TYPES.MILES,
            false
          )
        }
      ) );
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
    case actionTypes.UPDATE_COST_TO_ACTION_PLAN: {
      const nextPlanItems = updateActionPlan(
        state,
        action.data.routeIndex,
        PLAN_TYPES.AVERAGE_COST,
        data.value
      );

      return assign( state, updateRouteData( state.routes, data.routeIndex, {
        actionPlanItems: nextPlanItems
      } ) );
    }
    case actionTypes.UPDATE_DAYS_TO_ACTION_PLAN: {
      const nextPlanItems = updateActionPlan(
        state,
        action.data.routeIndex,
        PLAN_TYPES.DAYS_PER_WEEK,
        data.value
      );

      return assign( state, updateRouteData( state.routes, data.routeIndex, {
        actionPlanItems: nextPlanItems
      } ) );
    }
    case actionTypes.UPDATE_MILES_TO_ACTION_PLAN: {
      const nextPlanItems = updateActionPlan(
        state,
        action.data.routeIndex,
        PLAN_TYPES.MILES,
        data.value
      );

      return assign( state, updateRouteData( state.routes, data.routeIndex, {
        actionPlanItems: nextPlanItems
      } ) );
    }
    case actionTypes.UPDATE_TIME_TO_ACTION_PLAN: {
      const nextPlanItems = updateActionPlan(
        state,
        action.data.routeIndex,
        PLAN_TYPES.TIME,
        data.value
      );

      return assign( state, updateRouteData( state.routes, data.routeIndex, {
        actionPlanItems: nextPlanItems
      } ) );
    }
    case actionTypes.UPDATE_TRANSIT_TIME_HOURS: {
      const updates = {
        transitTimeHours: data.value || '0'
      };

      if ( !hasTransitTimeMinutes( state, data ) ) {
        updates.transitTimeMinutes = '0';
      }

      return assign(
        state,
        updateRouteData( state.routes, data.routeIndex, updates )
      );
    }
    case actionTypes.UPDATE_TRANSIT_TIME_MINUTES: {
      const updates = {
        transitTimeMinutes: data.value || '0'
      };

      if ( !hasTransitTimeHours( state, data ) ) {
        updates.transitTimeHours = '0';
      }

      return assign(
        state,
        updateRouteData( state.routes, data.routeIndex, updates )
      );
    }
    case actionTypes.UPDATE_IS_MONTHLY_COST: {
      return assign( state, updateRouteData( state.routes, data.routeIndex, {
        isMonthlyCost: Boolean( data.value )
      } ) );
    }
    default:
      return state;
  }
}

export {
  addRouteOptionAction,
  clearAverageCostAction,
  clearDaysPerWeekAction,
  initialState,
  clearMilesAction,
  routeSelector,
  todoListSelector,
  hasTodo,
  updateTransportationAction,
  updateMilesAction,
  updateDaysPerWeekAction,
  updateAverageCostAction,
  updateCostToActionPlan,
  updateDaysToActionPlan,
  updateMilesToActionPlan,
  updateTimeToActionPlan,
  updateTransitTimeHoursAction,
  updateTransitTimeMinutesAction,
  updateIsMonthlyCostAction
};

export default routeOptionReducer;
