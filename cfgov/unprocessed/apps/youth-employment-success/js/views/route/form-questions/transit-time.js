import { checkDom, setInitFlag } from '@cfpb/cfpb-atomic-component/src/utilities/atomic-helpers.js';
import {
  routeSelector,
  updateTimeToActionPlan,
  updateTransitTimeHoursAction,
  updateTransitTimeMinutesAction
} from '../../../reducers/route-option-reducer';
import inputView from '../../input';

const CLASSES = Object.freeze( {
  CONTAINER: 'm-yes-transit-time',
  HOURS: 'js-yes-hours',
  MINUTES: 'js-yes-minutes',
  NOT_SURE: 'js-yes-not-sure'
} );

const NOT_SURE_MESSAGE = 'Looking up how long this trip takes was added to your to-do list.';

/**
 * TransitTimeView
 * @class
 *
 * @classdesc Initializes the organism.
 *
 * @param {HTMLNode} element The root DOM element for this view
 * @param {object} props Additional properties to be supplied to the view
 * @returns {Object} The view's public methods
 */
function transitTimeView( element, { store, routeIndex, todoNotification } ) {
  const _dom = checkDom( element, CLASSES.CONTAINER );
  const _hoursEl = _dom.querySelector( `.${ CLASSES.HOURS }` );
  const _minutesEl = _dom.querySelector( `.${ CLASSES.MINUTES }` );
  const _notSureEl = _dom.querySelector( `.${ CLASSES.NOT_SURE }` );
  let _minutesView;
  let _hoursView;

  const _actionMap = {
    timeToActionPlan: updateTimeToActionPlan,
    transitTimeHours: updateTransitTimeHoursAction,
    transitTimeMinutes: updateTransitTimeMinutesAction
  };

  /**
   * Updates form state from child input text nodes
   * @param {object} updateObject object with DOM event and field name
   */
  function _setResponse( { name, event, value } ) {
    const method = _actionMap[name];
    const type = event.target.type;
    const finalValue = type === 'checkbox' ? event.target.checked : value;

    if ( type === 'checkbox' ) {
      if ( finalValue ) {
        todoNotification.show( NOT_SURE_MESSAGE );
      } else {
        todoNotification.hide();
      }
    }

    if ( method ) {
      store.dispatch( method( {
        routeIndex, value: finalValue } ) );
    }
  }

  /**
   * Re-render child components when state changes
   * @param {Object} _ The previous application state (unused)
   * @param {Object} state The current application state
   * @param {Object} state.routes The route objects currently stored in the application state
   */
  function _handleStateUpdate( _, state ) {
    const route = routeSelector( state.routes, routeIndex );

    _hoursView.render( route.transitTimeHours );
    _minutesView.render( route.transitTimeMinutes );
  }

  /**
   * Initialize the input elements this form manages
   */
  function _initInputs() {
    const textInputProps = {
      events: {
        blur: _setResponse
      },
      type: 'text'
    };

    _minutesView = inputView( _minutesEl, textInputProps );
    _hoursView = inputView( _hoursEl, textInputProps );

    inputView( _notSureEl, {
      events: {
        input: _setResponse
      },
      type: 'checkbox'
    } ).init();

    _hoursView.init();
    _minutesView.init();
  }

  return {
    init() {
      if ( setInitFlag( _dom ) ) {
        _initInputs();
        todoNotification.init( _dom );
        store.subscribe( _handleStateUpdate );
      }
    }
  };
}

transitTimeView.CLASSES = CLASSES;

export default transitTimeView;
