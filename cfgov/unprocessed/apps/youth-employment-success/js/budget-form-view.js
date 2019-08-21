import { checkDom, setInitFlag } from '../../../js/modules/util/atomic-helpers';
import inputView from './input-view';
import money from './money';

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
function BudgetFormView( element ) {
  const _dom = checkDom( element, CLASSES.FORM );
  const _state = {
    earned: '',
    spent: ''
  };

  /**
   *
   * @param {string} target The piece of state to be updated
   * @returns {function} A function that accepts an event and updates
   *  the state with the event target's value
   */
  function _handleInput( target ) {
    return ( { event } ) => {
      const amount = event.currentTarget.value;
      _state[target] = amount;
    };
  }

  const _handleEarnedInput = _handleInput( 'earned' );
  const _handleSpentInput = _handleInput( 'spent' );

  const _moneyEarnedEl = inputView(
    _dom.querySelector( `.${ CLASSES.EARNED_INPUT }` ),
    {
      events: {
        input: _handleEarnedInput,
        blur: _updateTotal
      }
    }
  );
  const _moneySpentEl = inputView(
    _dom.querySelector( `.${ CLASSES.SPENT_INPUT }` ),
    {
      events: {
        input: _handleSpentInput,
        blur: _updateTotal
      }
    }
  );
  const _moneyRemainingEl = _dom.querySelector( `.${ CLASSES.REMAINING }` );

  /**
   * Update dom node with amount remaining in user's budget
   */
  function _updateTotal() {
    const { earned, spent } = _state;

    _moneyRemainingEl.textContent = money.subtract( earned, spent );
  }

  return {
    init() {
      if ( setInitFlag( _dom ) ) {
        _moneyEarnedEl.init();
        _moneySpentEl.init();
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
