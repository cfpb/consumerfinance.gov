import { actionCreator, assign } from '../util';

const initialState = {
  selectedTransportation: [],
  daysPerWeek: '',
  miles: '',
  dailyCost: ''
};
const actionTypes = {
  UPDATE_TRANSPORTATION: 'UPDATE_TRANSPORTATION',
  UPDATE_MILES: 'UPDATE_MILES',
  UPDATE_DAILY_COST: 'UPDATE_DAILY_COST',
  UPDATE_DAYS_PER_WEEK: 'UPDATE_DAYS_PER_WEEK'
};

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
 * @param {object} state the current state of the reducer
 * @param {string} nextSelection the item to add or remove from the
 *  array of selected transportation options
 * @returns {array} the new transportation option array
 */
function updateTransportation( state, nextSelection ) {
  const { selectedTransportation: transportation } = state;
  const index = transportation.indexOf( nextSelection );

  if ( index > -1 ) {
    transportation.splice( index, 1 );
  } else {
    transportation.push( nextSelection );
  }

  return transportation;
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
    case actionTypes.UPDATE_DAILY_COST: {
      return assign( state, { dailyCost: data } );
    }
    case actionTypes.UPDATE_DAYS_PER_WEEK: {
      return assign( state, { daysPerWeek: data } );
    }
    case actionTypes.UPDATE_MILES: {
      return assign( state, { miles: data } );
    }
    case actionTypes.UPDATE_TRANSPORTATION: {
      return assign( state, {
        selectedTransportation: updateTransportation( state, data )
      } );
    }
    default:
      return state;
  }
}

export {
  initialState,
  updateTransportationAction,
  updateMilesAction,
  updateDaysPerWeekAction,
  updateDailyCostAction
};

export default routeOptionReducer;
