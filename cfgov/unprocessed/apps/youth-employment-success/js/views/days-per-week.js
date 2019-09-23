import { checkDom, setInitFlag } from '../../../../js/modules/util/atomic-helpers';
import {
  clearDaysPerWeekAction,
  routeSelector,
  updateDaysPerWeekAction,
  updateDaysToActionPlan
} from '../reducers/route-option-reducer';
import inputView from './input';

const CLASSES = Object.freeze( {
  CONTAINER: 'm-yes-days-per-week'
} );

/**
 * DaysPerWeekView
 * @class
 *
 * @classdesc View handles form elements related to the daysPerWeek field, including the
 * 'not sure' checkbox
 *
 * @param {HTMLNode} element The root DOM element for this view
 * @returns {Object} This view's public methods
 */
function daysPerWeekView( element, { store, routeIndex } ) {
  const _dom = checkDom( element, CLASSES.CONTAINER );
  const _daysPerWeekEl = _dom.querySelector( 'input[type="text"]' );
  const _notSureEl = _dom.querySelector( 'input[type="checkbox"]' );

  /**
   * Dispatch to the store the estimated cost the user anticipates
   * for their selected transportation option
   * @param {object} param0 The emitted DOM event
   */
  function _handleDaysUpdate( { event } ) {
    store.dispatch( updateDaysPerWeekAction( {
      routeIndex,
      value: event.target.value
    } ) );
  }

  /**
   * Dispatch to the store whether or not the user has indicated they
   * are unsure about the average cost of their selected transportation
   * option
   * @param {object} param0 The emitted DOM event
   */
  function _handleNotSureUpdate( { event } ) {
    store.dispatch( updateDaysToActionPlan( {
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
    const prevRouteState = routeSelector( prevState, routeIndex );
    const routeState = routeSelector( state, routeIndex );

    if ( routeState.transportation === 'Drive' ) {
      _dom.classList.remove( 'u-hidden' );
    } else {
      _daysPerWeekEl.value = '';
      _notSureEl.checked = '';
      if ( !_dom.classList.contains( 'u-hidden' ) ) {
        _dom.classList.add( 'u-hidden' );
      }

      if ( prevRouteState.daysPerWeek ) {
        store.dispatch( clearDaysPerWeekAction( { routeIndex } ) );
      }
    }
  }

  /**
   * Initial the input elements this view manages.
   */
  function _initInputs() {
    inputView( _daysPerWeekEl, {
      events: {
        input: _handleDaysUpdate
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

daysPerWeekView.CLASSES = CLASSES;

export default daysPerWeekView;
