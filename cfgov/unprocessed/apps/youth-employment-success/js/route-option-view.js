import { checkDom, setInitFlag } from '../../../js/modules/util/atomic-helpers';
import { assign } from './util';
import inputView from './input-view';

const CLASSES = Object.freeze( {
  FORM: 'o-yes-route-option',
  TRANSPORTATION_CHECKBOX: 'a-yes-route-mode',
  QUESTION_INPUT: 'a-yes-question'
} );

const defaultState = {
  selectedTransportation: [],
  daysPerWeek: '',
  miles: '',
  dailyCost: ''
};

/**
 * RouteOptionFormView
 * @class
 *
 * @classdesc Initializes the organism.
 *
 * @param {HTMLNode} element
 *  The root DOM element for this view
 * @returns {Object} The view's public methods
 */
function RouteOptionFormView( element ) {
  const state = assign( {}, defaultState );

  const _dom = checkDom( element, CLASSES.FORM );
  const _transportationTypes = Array.prototype.slice.call(
    _dom.querySelectorAll( `.${ CLASSES.TRANSPORTATION_CHECKBOX }` )
  );
  const _textInputs = Array.prototype.slice.call(
    _dom.querySelectorAll( `.${ CLASSES.QUESTION_INPUT }` )
  );

  /**
   * Updates form state from child input text nodes
   * @param {object} updateObject object with DOM event and field name
   */
  function _setQuestionResponse( { name, event } ) {
    state[name] = event.target.value;
  }

  /**
   * Updates state from child input checkbox nodes
   * @param {object} updateObject object with DOM event and field name
   */
  function _setChecked( { event } ) {
    const { selectedTransportation } = state;
    const { target: { value }} = event;
    const index = selectedTransportation.indexOf( value );

    if ( index > -1 ) {
      selectedTransportation.splice( index, 1 );
    } else {
      selectedTransportation.push( value );
    }

    state.selectedTransportation = selectedTransportation;
  }

  /**
   * Initialize checkbox nodes this form view manages
   */
  function _initRouteOptions() {
    _transportationTypes.forEach( node => inputView( node, {
      events: { click: _setChecked },
      type: 'checkbox'
    } )
      .init()
    );
  }

  /**
   * Initialize input nodes this form view manages
   */
  function _initQuestions() {
    _textInputs.forEach( node => inputView( node, {
      events: { input: _setQuestionResponse }
    } )
      .init()
    );
  }

  return {
    init() {
      if ( setInitFlag( _dom ) ) {
        _initRouteOptions();
        _initQuestions();
      }
    }
  };
}

RouteOptionFormView.CLASSES = CLASSES;

export default RouteOptionFormView;
