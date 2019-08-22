import { actionCreator, assign } from '../util';

export const initialState = {
  earned: '',
  spent: ''
};

export const actionTypes = {
  UPDATE_EARNED: 'UPDATE_EARNED',
  UPDATE_SPENT: 'UPDATE_SPENT'
};

export const updateEarnedAction = actionCreator( actionTypes.UPDATE_EARNED );
export const updateSpentAction = actionCreator( actionTypes.UPDATE_SPENT );

/**
 *
 * @param {object} state the current values for this slice of app state
 * @param {object} action instructs reducer which state update to apply
 * @returns {object} the updated state object
 */
function budgetReducer( state = initialState, action ) {
  const { type, data } = action;

  switch ( type ) {
    case actionTypes.UPDATE_EARNED: {
      return assign( state, { earned: data } );
    }
    case actionTypes.UPDATE_SPENT: {
      return assign( state, { spent: data } );
    }
    default:
      return state;
  }
}

export default budgetReducer;
