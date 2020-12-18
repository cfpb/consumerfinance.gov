import { checkDom, setInitFlag } from '@cfpb/cfpb-atomic-component/src/utilities/atomic-helpers.js';
import { toArray } from '../../util';

const CLASSES = Object.freeze( {
  CONTAINER: 'js-your-goals',
  GOAL: 'js-review-goal'
} );

const DATA_ATTR = 'data-js-goal';

/**
 * ReviewGoalsView
 *
 * @class
 *
 * @classdesc View to display user's indicated goals in the review section
 * of the transit tool
 *
 * @param {HTMLElement} element The container node for this view
 * @param {Object} props The additional properties supplied to this view
 * @param {YesStore} props.store The public API exposed by the Store class
 * @returns {Object} This view's public API
 */
function reviewGoalsView( element, { store } ) {
  const _dom = checkDom( element, CLASSES.CONTAINER );
  const _goalsMap = toArray(
    _dom.querySelectorAll( `.${ CLASSES.GOAL }` )
  )
    .reduce( ( memo, el ) => {
      memo[el.getAttribute( DATA_ATTR )] = el;

      return memo;
    }, {} );

  /**
   * Predicate function to determine if DOM updates should be made
   * @param {Object} prevState The last application state
   * @param {Object} state The current application state
   * @returns {Boolean} Whether or not the DOM should update
   */
  function _shouldUpdate( prevState, state ) {
    const prevGoals = prevState.goals || {};
    const goals = state.goals;
    let shouldUpdate = false;

    if ( !Object.keys( prevGoals ).length ) {
      return true;
    }

    for ( const goal in prevGoals ) {
      if ( prevGoals.hasOwnProperty( goal ) ) {
        const prevGoalContent = prevGoals[goal];
        const goalContent = goals[goal];

        if ( goalContent !== prevGoalContent ) {
          shouldUpdate = true;
          return shouldUpdate;
        }
      }
    }

    return shouldUpdate;
  }

  /**
   * Event handler to update DOM with current state
   * @param {Object} prevState The last application state
   * @param {Object} state The current application state
   */
  function _handleStateUpdate( prevState, state ) {
    const { goals } = state;

    if ( _shouldUpdate( prevState, state ) ) {
      for ( const attr in _goalsMap ) {
        if ( _goalsMap.hasOwnProperty( attr ) ) {
          const el = _goalsMap[attr];

          el.innerHTML = goals[attr] || '';
        }
      }
    }
  }

  return {
    init() {
      if ( setInitFlag( _dom ) ) {
        _handleStateUpdate( {}, store.getState() );
        store.subscribe( _handleStateUpdate );
      }
    }
  };
}

reviewGoalsView.CLASSES = CLASSES;

export default reviewGoalsView;
