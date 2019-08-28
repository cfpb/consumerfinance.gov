import { actionCreator, assign } from '../util';

const initialState = {
  transportation: '',
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
        transportation: data
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
