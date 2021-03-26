import { checkDom, setInitFlag } from '@cfpb/cfpb-atomic-component/src/utilities/atomic-helpers.js';
import {
  updateEarnedAction,
  updateSpentAction
} from '../../reducers/budget-reducer';
import { formatNegative, toPrecision } from '../../util';
import inputView from '../input';
import money from '../../money';

const CLASSES = Object.freeze( {
  FORM: 'o-yes-budget',
  EARNED_INPUT: 'o-yes-budget-earned',
  SPENT_INPUT: 'o-yes-budget-spent',
  REMAINING: 'o-yes-budget-remaining'
} );

/**
 * BudgetFormView
 * @class
 *
 * @classdesc Initializes the organism.
 *
 * @param {HTMLElement} element
 *  The root DOM element for this view
 * @returns {object} The view's public methods
 */
function BudgetFormView( element, { store } ) {
  const _dom = checkDom( element, CLASSES.FORM );

  /**
   *
   * @param {function} action The action object to be dispatched to the store
   * @returns {Function} A function that accepts an event and updates
   *  the state with the event target's value
   */
  function _handleInput( action ) {
    return ( { _, value } ) => {
      store.dispatch( action( value ) );
    };
  }

  const _handleEarnedInput = _handleInput( updateEarnedAction );
  const _handleSpentInput = _handleInput( updateSpentAction );

  /**
   * Update the input element with formatted value, dispatch that value to the store
   * @param {Object} updateObj Object with updated data from form control event dispatch
   * @param {Object} updateObj.event The raw DOM event
   * @param {Object} updateObj.value The value of the form control element
   */
  function _handleEarnedBlur( { event, value } ) {
    event.target.value = toPrecision( value, 2 );
    _handleEarnedInput( { event, value: event.target.value } );
  }

  /**
   * Update the input element with formatted value, dispatch that value to the store
   * @param {Object} updateObj Object with updated data from form control event dispatch
   * @param {Object} updateObj.event The raw DOM event
   * @param {Object} updateObj.value The value of the form control element
   */
  function _handleSpentBlur( { event, value } ) {
    event.target.value = value ? toPrecision( value, 2 ) : '';
    _handleSpentInput( { event, value: event.target.value } );
  }

  const _moneyEarnedEl = inputView(
    _dom.querySelector( `.${ CLASSES.EARNED_INPUT }` ),
    {
      events: {
        input: _handleEarnedInput,
        blur: _handleEarnedBlur
      }
    }
  );
  const _moneySpentEl = inputView(
    _dom.querySelector( `.${ CLASSES.SPENT_INPUT }` ),
    {
      events: {
        input: _handleSpentInput,
        blur: _handleSpentBlur
      }
    }
  );
  const _moneyRemainingEl = _dom.querySelector( `.${ CLASSES.REMAINING }` );

  /**
   * Update dom node with amount remaining in user's budget
   * @param {Object} _ The previous state of the store
   * @param {Object} state The current state of the store
   * @param {Object} state.budget The current budget state
   */
  function _updateTotal( _, { budget } ) {
    const { earned, spent } = budget;
    const total = !earned && !spent ? '-' : toPrecision( money.subtract( earned, spent ), 2 );

    _moneyRemainingEl.innerHTML = formatNegative( total );
  }

  return {
    init() {
      if ( setInitFlag( _dom ) ) {
        _moneyEarnedEl.init();
        _moneySpentEl.init();
        store.subscribe( _updateTotal );
      }
    },

    destroy() {
      _moneyEarnedEl.destroy();
      _moneySpentEl.destroy();
    }
  };
}

BudgetFormView.CLASSES = CLASSES;

export default BudgetFormView;
