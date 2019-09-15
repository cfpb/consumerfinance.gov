import { assign, entries } from '../util';
import { setInitFlag } from '../../../../js/modules/util/atomic-helpers';

const defaultProps = {
  type: 'text'
};
const NODE_MISSING_ERROR = 'InputView expects to be initialized with an input node matching the supplied `type` prop';

function isInputNode(element) {
  if (
    element instanceof HTMLInputElement ||
    element instanceof HTMLTextAreaElement
  ) {
    return true;
  }

  return false;
}

/**
 * Get the correct DOM node this view controls
 * @param {node} element dom node representing either the input this
 *  view controls or it's parent
 * @param {*} type the kind of input (text, checkbox, etc)
 * @returns {node} The final dom node for this view
 */
function resolve( element, type ) {
  if ( isInputNode(element) ) {
    return element;
  }

  return element.querySelector( `input[type="${ type }"]` );
}

/**
 * InputView
 * Generic view for input elements
 * @class
 *
 * @classdesc Initializes the molecule.
 *
 * @param {HTMLNode} element The root DOM element for this view
 * @param {Object} props Properties the view should be initialized with
 * @returns {Object} The view's public methods
 */
function inputView( element, props = {} ) {
  const _finalProps = assign( {}, defaultProps, props );
  const _dom = resolve( element, _finalProps.type );

  const _eventsMap = {};

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
    const fieldName = target.getAttribute( 'data-js-name' ) || target.name;

    return handler( { name: fieldName, event } );
  };

  /**
   * Bind event handers to nodes this view manages
   * Each event is stored in an object to facilitate unbinding when
   * necessary
   */
  function _bindEvents() {
    const { events = {}} = props;
    const eventHandlers = entries( events );

    eventHandlers.forEach( ( [ event, handler ] ) => {
      const handlerCache = _eventsMap[event] || [];
      const delegate = eventHandler( handler );
      handlerCache.push( delegate );

      _dom.addEventListener( event, delegate );

      _eventsMap[event] = handlerCache;
    } );
  }

  /**
   * Unbind all event handlers from the input
   */
  function _unbindEvents() {
    const events = entries( _eventsMap );

    events.forEach( ( [ event, handlers ] ) => {
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
export default inputView;
