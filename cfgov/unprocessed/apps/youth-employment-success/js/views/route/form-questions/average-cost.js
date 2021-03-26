import { checkDom, setInitFlag } from '@cfpb/cfpb-atomic-component/src/utilities/atomic-helpers.js';
import {
  clearAverageCostAction,
  routeSelector,
  updateAverageCostAction,
  updateCostToActionPlan,
  updateIsMonthlyCostAction
} from '../../../reducers/route-option-reducer';
import inputView from '../../input';
import { toArray, toPrecision } from '../../../util';

const CLASSES = Object.freeze( {
  CONTAINER: 'm-yes-average-cost',
  RADIO: 'a-radio'
} );

const COST_FREQUENCY_TYPES = {
  DAILY: 'daily',
  MONTHLY: 'monthly'
};

const NOT_SURE_MESSAGE = 'Looking up average cost was added to your to-do list.';

/**
 * AverageCostView
 * @class
 *
 * @classdesc View handles form elements related to the averageCost field, including the
 * 'not sure' checkbox and daily/monthly radio buttons
 *
 * @param {HTMLNode} element The root DOM element for this view
 * @returns {Object} This view's public methods
 */
function averageCostView( element, { store, routeIndex, todoNotification } ) {
  const _dom = checkDom( element, CLASSES.CONTAINER );
  const _averageCostEl = _dom.querySelector( 'input[type="text"]' );
  const _radioEls = toArray( _dom.querySelectorAll( `.${ CLASSES.RADIO }` ) );
  const _notSureEl = _dom.querySelector( 'input[type="checkbox"]' );

  /**
   * Dispatch to the store which cost-frequency radio button
   * the user has selected.
   * @param {object} inputData The data returned from the InputView's event handler function
   * @param {object} inputData.event The emitted DOM event
   * @param {string} inputData.name The name of the field the event was emitted from
   */
  function _handleFrequencySelection( { event } ) {
    const type = event.target.value;
    const costFrequencyFlag = type === COST_FREQUENCY_TYPES.MONTHLY;

    store.dispatch( updateIsMonthlyCostAction( {
      routeIndex,
      value: costFrequencyFlag
    } ) );
  }

  /**
   * Dispatch to the store the estimated cost the user anticipates
   * for their selected transportation option
   * @param {object} updateObject The data returned from the InputView's event handler function
   * @param {object} updateObject.event The emitted DOM event
   * @param {string} updateObject.name The name of the field the event was emitted from
   */
  function _handleAverageCostUpdate( { event, value } ) {
    store.dispatch( updateAverageCostAction( {
      routeIndex,
      value
    } ) );
  }

  /**
   * Dispatch to the store whether or not the user has indicated they
   * are unsure about the average cost of their selected transportation
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

    store.dispatch( updateCostToActionPlan( {
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

    if ( prevRouteState.transportation !== routeState.transportation ) {
      if ( routeState.transportation === 'Drive' ) {
        _averageCostEl.value = '';
        _notSureEl.checked = '';
        _radioEls.forEach( radio => { radio.checked = ''; } );
        _dom.classList.add( 'u-hidden' );
        todoNotification.remove();
        store.dispatch( clearAverageCostAction( { routeIndex } ) );
      } else {
        _dom.classList.remove( 'u-hidden' );
      }
    }
  }

  function _handleBlur( { event, value } ) {
    event.target.value = value ? toPrecision( value, 2 ) : '';
    _handleAverageCostUpdate( { event, value: event.target.value } );
  }

  /**
   * Initial the input elements this view manages.
   */
  function _initInputs() {
    inputView( _averageCostEl, {
      events: {
        input: _handleAverageCostUpdate,
        blur: _handleBlur
      }
    } ).init();

    _radioEls.forEach( node => {
      inputView( node, {
        events: {
          click: _handleFrequencySelection
        },
        type: 'radio'
      } ).init();
    } );

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
        todoNotification.init( _dom );
        store.subscribe( _onStateUpdate );
      }
    }
  };
}

averageCostView.CLASSES = CLASSES;

export default averageCostView;
