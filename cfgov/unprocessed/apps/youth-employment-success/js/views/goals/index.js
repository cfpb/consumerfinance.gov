import { checkDom, setInitFlag } from '@cfpb/cfpb-atomic-component/src/utilities/atomic-helpers.js';
import {
  updateGoalAction,
  updateGoalImportanceAction,
  updateGoalStepsAction,
  updateGoalTimelineAction
} from '../../reducers/goal-reducer';
import inputView from '../input';
import { toArray } from '../../util';

const CLASSES = {
  CONTAINER: 'js-yes-goals',
  LONG_TERM_GOAL: 'js-long-term-goal',
  GOAL_IMPORTANCE: 'js-goal-importance',
  GOAL_STEPS: 'js-goal-steps',
  GOAL_TIMELINE: 'a-radio'
};

const GOALS_TO_ACTIONS = {
  longTermGoal: updateGoalAction,
  goalImportance: updateGoalImportanceAction,
  goalSteps:  updateGoalStepsAction
};

const NEWLINE_REGEXP = /(?:\r\n)|\r|\n/g;

/**
 * GoalsView
 * @class
 *
 * @classdesc View managing form controls in the prelimiary goals section
 *
 * @param {HTMLNode} element The root DOM element for this view
 * @param {Object} props Additional properties to be supplied to the view
 * @params {Object} props.store The app state store
 * @returns {Object} The view's public methods
 */
function goalsView( element, { store } ) {
  const _dom = checkDom( element, CLASSES.CONTAINER );

  /**
  * Dispatch to the store the value of the last blurred goals section textarea node.
  * @param {object} updateObject The data returned from the InputView's event handler function
  * @param {object} updateObject.event The emitted DOM event
  * @param {string} updateObject.name The name of the field the event was emitted from
  */
  function _handleUpdateGoals( { name, event } ) {
    const method = GOALS_TO_ACTIONS[name];

    if ( method ) {
      const textHTMLNewlines = event.target.value.replace( NEWLINE_REGEXP, '<br />' );
      store.dispatch( method( textHTMLNewlines ) );
    }
  }

  /**
  * Dispatch to the store which timeline radio button the user has selected.
  * @param {object} updateObject The data returned from the InputView's event handler function
  * @param {object} updateObject.event The emitted DOM event
  * @param {string} updateObject.name The name of the field the event was emitted from
  */
  function _handleTimelineUpdate( { event } ) {
    store.dispatch( updateGoalTimelineAction(
      event.target.value
    ) );
  }

  /**
   * Initialize form control views
   */
  function _initInputs() {
    [
      CLASSES.LONG_TERM_GOAL,
      CLASSES.GOAL_IMPORTANCE,
      CLASSES.GOAL_STEPS
    ].forEach( klass => {
      inputView( _dom.querySelector( `.${ klass }` ), {
        events: {
          blur: _handleUpdateGoals
        }
      } ).init();
    } );

    toArray(
      _dom.querySelectorAll( `.${ CLASSES.GOAL_TIMELINE }` )
    ).forEach( radio => {
      inputView( radio, {
        events: {
          click: _handleTimelineUpdate
        },
        type: 'radio'
      } ).init();
    } );
  }

  return {
    init() {
      if ( setInitFlag( _dom ) ) {
        _initInputs();
      }
    }
  };
}

goalsView.CLASSES = CLASSES;

export default goalsView;
