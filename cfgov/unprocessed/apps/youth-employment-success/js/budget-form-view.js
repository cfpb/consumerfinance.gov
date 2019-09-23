import { checkDom, setInitFlag } from '../../../js/modules/util/atomic-helpers';
import {
  updateEarnedAction,
  updateSpentAction
} from './reducers/budget-reducer';
import inputView from './views/input';
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
function BudgetFormView( element, { store } ) {
  const _dom = checkDom( element, CLASSES.FORM );

  /* might be useful to have a `connect` function that exposes mapState and mapDispatch to props
     for better separation of concerns */
  store.subscribe( () => {
    _updateTotal( store.getState() );
  } );

  /**
   *
   * @param {function} action The action object to be dispatched to the store
   * @returns {Function} A function that accepts an event and updates
   *  the state with the event target's value
   */
  function _handleInput( action ) {
    return ( { event } ) => {
      const amount = event.currentTarget.value;
      store.dispatch( action( amount ) );
    };
  }

  const _handleEarnedInput = _handleInput( updateEarnedAction );
  const _handleSpentInput = _handleInput( updateSpentAction );

  const _moneyEarnedEl = inputView(
    _dom.querySelector( `.${ CLASSES.EARNED_INPUT }` ),
    {
      events: {
        input: _handleEarnedInput
      }
    }
  );
  const _moneySpentEl = inputView(
    _dom.querySelector( `.${ CLASSES.SPENT_INPUT }` ),
    {
      events: {
        input: _handleSpentInput
      }
    }
  );
  const _moneyRemainingEl = _dom.querySelector( `.${ CLASSES.REMAINING }` );

  /**
   * Update dom node with amount remaining in user's budget
   */
  function _updateTotal( { budget } ) {
    const { earned, spent } = budget;

    _moneyRemainingEl.textContent = money.subtract( earned, spent );
  }

  return {
    init() {
      if ( setInitFlag( _dom ) ) {
        _moneyEarnedEl.init();
        _moneySpentEl.init();
        _updateTotal( store.getState() );
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
