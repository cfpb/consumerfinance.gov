import { actionCreator, assign } from '../util';

const initialState = {
  routes: []
};

const actionTypes = Object.freeze( {
  ADD_ROUTE_OPTION: 'ADD_ROUTE_OPTION',
  UPDATE_TRANSPORTATION: 'UPDATE_TRANSPORTATION',
  UPDATE_MILES: 'UPDATE_MILES',
  UPDATE_DAILY_COST: 'UPDATE_DAILY_COST',
  UPDATE_DAYS_PER_WEEK: 'UPDATE_DAYS_PER_WEEK'
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
const updateDailyCostAction = actionCreator(
  actionTypes.UPDATE_DAILY_COST
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
    case actionTypes.UPDATE_DAILY_COST: {
      return assign( state, updateRouteData(
        state.routes,
        data.routeIndex,
        { dailyCost: data.value } )
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
  updateDailyCostAction
};

export default routeOptionReducer;
