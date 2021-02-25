import { checkDom, setInitFlag } from '@cfpb/cfpb-atomic-component/src/utilities/atomic-helpers.js';
import {
  clearMilesAction,
  hasTodo,
  routeSelector,
  updateMilesAction,
  updateMilesToActionPlan
} from '../../../reducers/route-option-reducer';
import { PLAN_TYPES } from '../../../data-types/todo-items';
import inputView from '../../input';

const CLASSES = Object.freeze( {
  CONTAINER: 'm-yes-miles'
} );

const NOT_SURE_MESSAGE = 'Looking up how many miles you drive each day was added to your to-do list.';

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
function milesView( element, { store, routeIndex, todoNotification } ) {
  const _dom = checkDom( element, CLASSES.CONTAINER );
  const _milesEl = _dom.querySelector( 'input[type="text"]' );
  const _notSureEl = _dom.querySelector( 'input[type="checkbox"]' );

  /**
   * Dispatch to the store the number of miles theuy expect to drive in a day.
   * @param {object} updateObject The data returned from the InputView's event handler function
   * @param {object} updateObject.event The emitted DOM event
   * @param {string} updateObject.name The name of the field the event was emitted from
   */
  function _handleUpdateMiles( { event, value } ) {
    store.dispatch( updateMilesAction( {
      routeIndex,
      value
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
    const { checked } = event.target;

    if ( checked ) {
      todoNotification.show( NOT_SURE_MESSAGE );
    } else {
      todoNotification.hide();
    }

    store.dispatch( updateMilesToActionPlan( {
      routeIndex,
      value: checked
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
    const routeState = routeSelector( state.routes, routeIndex );
    const prevRouteState = routeSelector( prevState.routes, routeIndex );

    if ( routeState.transportation === 'Drive' ) {
      _dom.classList.remove( 'u-hidden' );
    } else {
      _milesEl.value = '';
      _notSureEl.checked = '';
      _dom.classList.add( 'u-hidden' );
      todoNotification.remove();

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
        todoNotification.init( _dom );
      }
    }
  };
}

milesView.CLASSES = CLASSES;

export default milesView;
