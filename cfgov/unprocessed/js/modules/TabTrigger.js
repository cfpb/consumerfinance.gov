// Required modules.
import EventObserver from '@cfpb/cfpb-atomic-component/src/mixins/EventObserver.js';

// Key code for the tab key on the keyboard.
const KEY_TAB = 9;

/**
 * Dynamically creates an HTML element and attaches it to a DOM node.
 * @param  {string} type - The type of HTML node to create.
 * @param  {HTMLNode} target - An HTML element to insert the new node into.
 * @returns {HTMLNode} The newly created HTML node.
 */
function createElement( type, target ) {
  const elem = document.createElement( type );
  target.appendChild( elem );
  return elem;
}

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

  const _this = this;

  /**
   * @returns {TabTrigger} An instance.
   */
  function init() {
    const _tabTriggerDom = createElement( 'button', element );
    _tabTriggerDom.className = 'u-tab-trigger u-visually-hidden';
    _tabTriggerDom.setAttribute( 'aria-hidden', 'true' );

    /*
    The tab trigger is hidden, but is used to listen for keyup events
    when the tab key is pressed on it while it has focus, so that
    the menu can be collapsed.
     */
    _tabTriggerDom.innerText = 'Collapse';

    _tabTriggerDom.addEventListener( 'keyup', _handleTabPress );

    return this;
  }

  /**
   * Event handler for when the tab key is pressed.
   * @param {KeyboardEvent} event
   *   The event object for the keyboard key press.
   */
  function _handleTabPress( event ) {
    if ( event.keyCode === KEY_TAB ) {
      _this.dispatchEvent( 'tabPressed' );
    }
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
