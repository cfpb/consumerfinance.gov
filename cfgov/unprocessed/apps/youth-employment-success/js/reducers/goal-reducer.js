import { actionCreator, assign } from '../util';

const GOAL_TIMELINES = [
  '3 to 6 months',
  '6 to 9 months',
  '9 months to 1 year',
  '1 year or more'
];

const TYPES = {
  UPDATE_LONG_TERM_GOAL: 'UPDATE_LONG_TERM_GOAL',
  UPDATE_GOAL_IMPORTANCE: 'UPDATE_GOAL_IMPORTANCE',
  UPDATE_GOAL_STEPS: 'UPDATE_GOAL_STEPS',
  UPDATE_GOAL_TIMELINE: 'UPDATE_GOAL_TIMELINE'
};

const initialState = {
  longTermGoal: '',
  goalImportance: '',
  goalSteps: '',
  goalTimeline: ''
};

const handlers = {
  UPDATE_LONG_TERM_GOAL: updateGoal,
  UPDATE_GOAL_IMPORTANCE: updateImportance,
  UPDATE_GOAL_STEPS: updateSteps,
  UPDATE_GOAL_TIMELINE: updateTimeline
};

const updateGoalAction = actionCreator(
  TYPES.UPDATE_LONG_TERM_GOAL
);
const updateGoalImportanceAction = actionCreator(
  TYPES.UPDATE_GOAL_IMPORTANCE
);
const updateGoalStepsAction = actionCreator(
  TYPES.UPDATE_GOAL_STEPS
);
const updateGoalTimelineAction = actionCreator(
  TYPES.UPDATE_GOAL_TIMELINE
);

/**
 *
 * @param {object} state the current values for this slice of app state
 * @param {object} action instructs reducer which state update to apply
 * @returns {object} the updated state object
 */
function updateGoal( state, action ) {
  return assign( state, {
    longTermGoal: action.data.value
  } );
}

/**
 *
 * @param {object} state the current values for this slice of app state
 * @param {object} action instructs reducer which state update to apply
 * @returns {object} the updated state object
 */
function updateImportance( state, action ) {
  return assign( state, {
    goalImportance: action.data.value
  } );
}

/**
 *
 * @param {object} state the current values for this slice of app state
 * @param {object} action instructs reducer which state update to apply
 * @returns {object} the updated state object
 */
function updateSteps( state, action ) {
  return assign( state, {
    goalSteps: action.data.value
  } );
}

/**
 *
 * @param {object} state the current values for this slice of app state
 * @param {object} action instructs reducer which state update to apply
 * @returns {object} the updated state object
 */
function updateTimeline( state, action ) {
  const timeline = action.data;
  const validTimeline = GOAL_TIMELINES.includes( timeline ) ? timeline : '';

  return assign( state, {
    goalTimeline: validTimeline
  } );
}

/**
 *
 * @param {object} state the current values for this slice of app state
 * @param {object} action instructs reducer which state update to apply
 * @returns {object} the updated state object
 */
function goalReducer( state = initialState, action ) {
  if ( handlers.hasOwnProperty( action.type ) ) {
    const handler = handlers[action.type];
    return handler( state, action );
  }

  return state;
}

export {
  GOAL_TIMELINES,
  initialState,
  updateGoalAction,
  updateGoalImportanceAction,
  updateGoalStepsAction,
  updateGoalTimelineAction
};
export default goalReducer;
