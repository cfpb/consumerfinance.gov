import { actionCreator } from '../util';

const initialState = '';
const TYPES = {
  UPDATE_ROUTE_OPTION_CHOICE: 'UPDATE_ROUTE_OPTION_CHOICE'
};
const updateRouteChoiceAction = actionCreator(
  TYPES.UPDATE_ROUTE_OPTION_CHOICE
);

const isWaiting = state => state.routeChoice === 'wait';

function choiceReducer( state = initialState, action ) {
  switch ( action.type ) {
    case TYPES.UPDATE_ROUTE_OPTION_CHOICE: {
      return action.data;
    }
    default: {
      return state;
    }
  }
}

export {
  isWaiting,
  updateRouteChoiceAction
};

export default choiceReducer;
