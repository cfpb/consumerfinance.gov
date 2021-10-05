// Required modules.
import EventObserver from '@cfpb/cfpb-atomic-component/src/mixins/EventObserver.js';

/**
 * TabTrigger
 * @class
 *
 * @classdesc Initializes a new TabTrigger module.
 *
 * @param {HTMLNode} element
 *   The DOM element within which to search for the module's root node.
 * @returns {TabTrigger} An instance.
 */
function TabTrigger( element ) {

  /**
   * @returns {TabTrigger} An instance.
   */
  function init() {
    element.addEventListener( 'focusout', _handleFocusOut.bind( this ) );

    return this;
  }

  /**
   * @param {FocusEvent} event
   * @returns {boolean} True if tabPressed is dispatched, false otherwise.
   */
  function _handleFocusOut( event ) {
    /* If focus is still in the element, do nothing.
       The relatedTarget parameter is the EventTarget losing focus. */
    if ( element.contains( event.relatedTarget ) ) return false;

    this.dispatchEvent( 'tabPressed' );
    return true;
  }

  // Attach public events.
  const eventObserver = new EventObserver();
  this.addEventListener = eventObserver.addEventListener;
  this.removeEventListener = eventObserver.removeEventListener;
  this.dispatchEvent = eventObserver.dispatchEvent;

  this.init = init;

  return this;
}

export default TabTrigger;
