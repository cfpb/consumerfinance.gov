import { UNDEFINED } from './util';
import { setInitFlag } from '../../../js/modules/util/atomic-helpers';

const defaultProps = {
  type: 'text'
};
const NODE_MISSING_ERROR = 'InputView expects to be initialized with an input node matching the supplied `type` prop';

/**
 * Noop fallback for undefined event handlers
 * @returns {undefined} undefined
 */
function noop() {
  return UNDEFINED;
}

/**
 * Get the correct DOM node this view controls
 * @param {node} element dom node representing either the input this
 *  view controls or it's parent
 * @param {*} type the kind of input (text, checkbox, etc)
 * @returns {node} The final dom node for this view
 */
function resolve( element, type ) {
  if ( element instanceof HTMLInputElement ) {
    return element;
  }

  return element.querySelector( `input[type="${ type }"]` );
}

/**
 * InputView
 * Generic view for input elements
 * @class
 *
 * @classdesc Initializes the organism.
 *
 * @param {HTMLNode} element The root DOM element for this view
 * @param {Object} props Properties the view should be initialized with
 * @returns {Object} The view's public methods
 */
function InputView( element, props = {} ) {
  const finalProps = {
    ...defaultProps,
    ...props
  };
  const _dom = resolve( element, finalProps.type );

  const eventsMap = {};

  if ( !_dom ) {
    throw new Error( NODE_MISSING_ERROR );
  }

  /**
   *
   * @param {Function} handler event handler passed in through props
   * @returns {Function} A function that accepts an event and updates
   *  the state with the event target's value
   */
  const eventHandler = handler => event => {
    const { target } = event;
    // jinja2 auto double quotes attributes?
    const dataName = target.getAttribute( 'data-js-name' );
    const fieldName = ( dataName && dataName.slice( 1, -1 ) ) || target.name;

    return handler( { name: fieldName, event } );
  };

  /**
   * Bind event handers to nodes this view manages
   */
  function _bindEvents() {
    const { events = {}} = props;

    Object.entries( events ).forEach( ( [ event, handler = noop ] ) => {
      const handlerCache = eventsMap[event] || [];
      const delegate = eventHandler( handler );
      handlerCache.push( delegate );

      _dom.addEventListener( event, delegate );

      eventsMap[event] = handlerCache;
    } );
  }

  /**
   * Unbind all event handlers from the input
   */
  function _unbindEvents() {
    Object.entries( eventsMap ).forEach( ( [ event, handlers ] ) => {
      handlers.forEach( handler => _dom.removeEventListener( event, handler ) );
    } );
  }

  return {
    init() {
      if ( setInitFlag( element ) ) {
        _bindEvents();
      }
    },
    destroy() {
      _unbindEvents();
    }
  };
}

export { NODE_MISSING_ERROR };
export default InputView;
