import { checkDom, setInitFlag } from '../../../../js/modules/util/atomic-helpers';
import {
  clearMilesAction,
  hasTodo,
  routeSelector,
  updateMilesAction,
  updateMilesToActionPlan
} from '../reducers/route-option-reducer';
import inputView from '../input-view';
import { PLAN_TYPES } from '../data/todo-items';

const CLASSES = Object.freeze( {
  CONTAINER: 'm-yes-miles'
} );

/**
 * MilesView
 * @class
 *
 * @classdesc Manages form controls and corresponding DOM
 * manuipulation for the `miles per day` question.
 *
 * @param {HTMLNode} element
 *  The root DOM element for this view
 * @param {object} props The additional properties this object accepts
 * @param {object} props.store The app store instance
 * @param {string} props.routeIndex The index of the route option this view updates
 * @returns {Object} The view's public methods
 */
function milesView( element, { store, routeIndex } ) {
  const _dom = checkDom( element, CLASSES.CONTAINER );
  const _milesEl = _dom.querySelector( 'input[type="text"]' );
  const _notSureEl = _dom.querySelector( 'input[type="checkbox"]' );

  /**
   * Dispatch to the store the number of miles theuy expect to drive in a day.
   * @param {object} updateObject The data returned from the InputView's event handler function
   * @param {object} updateObject.event The emitted DOM event
   * @param {string} updateObject.name The name of the field the event was emitted from
   */
  function _handleUpdateMiles( { event } ) {
    store.dispatch( updateMilesAction( {
      routeIndex,
      value: event.target.value
    } ) );
  }

  /**
   * Dispatch to the store whether or not the user has indicated they
   * are unsure about how many miles per day they expect to drive.
   * option
   * @param {object} updateObject The data returned from the InputView's event handler function
   * @param {object} updateObject.event The emitted DOM event
   * @param {string} updateObject.name The name of the field the event was emitted from
   */
  function _handleNotSureUpdate( { event } ) {
    store.dispatch( updateMilesToActionPlan( {
      routeIndex,
      value: event.target.checked
    } ) );
  }

  /**
   * Toggles the visibility of the form controls depending on the
   * transportation option selected. Clears form field when toggled
   * to prevent calculation bugs.
   * @param {object} prevState The last state of the app.
   * @param {object} state The current state of the app.
   */
  function _onStateUpdate( prevState, state ) {
    const routeState = routeSelector( state, routeIndex );
    const prevRouteState = routeSelector( prevState, routeIndex );

    if ( routeState.transportation === 'Drive' ) {
      _dom.classList.remove( 'u-hidden' );
    } else {
      _milesEl.value = '';
      _notSureEl.checked = '';
      _dom.classList.add( 'u-hidden' );

      if (
        prevRouteState.miles ||
        hasTodo( prevRouteState.actionPlanItems, PLAN_TYPES.MILES )
      ) {
        store.dispatch( clearMilesAction( { routeIndex } ) );
      }
    }
  }

  /**
   * Initialze the form controls this view manages
   */
  function _initInputs() {
    inputView( _milesEl, {
      events: {
        input: _handleUpdateMiles
      }
    } ).init();

    inputView( _notSureEl, {
      events: {
        click: _handleNotSureUpdate
      },
      type: 'checkbox'
    } ).init();
  }

  return {
    init() {
      if ( setInitFlag( _dom ) ) {
        _initInputs();
        _dom.classList.add( 'u-hidden' );
        store.subscribe( _onStateUpdate );
      }
    }
  };
}

milesView.CLASSES = CLASSES;

export default milesView;
