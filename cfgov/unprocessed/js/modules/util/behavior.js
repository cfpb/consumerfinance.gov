/* ==========================================================================
   Dom Behaviors

   Behaviors are functionality that can be shared between different pieces
   of markup. They are not strictly atomic, though they likely are used
   on atomic components. An example of shared behavior may be a menu that
   expands and collapses and sets the aria-expanded attribute on the HTML.
   Or an input field that can be cleared by clicking an (x) button in the
   input. These are both behaviors that may appear in different parts of
   the codebase, but could share the same functionality.
   Behaviors are added through the `data-js-hook` attribute on the HTML
   and have a prefix of `behavior_`
   (both those designators are set in modules/util/standard-type.js).

   For example, `modules/behaviors/FlyoutMenu.js` defines the behavior of
   expanding and collapsing an expandable menu. At a minimum, three things
   need to be defined: (A) The containing scope of the menu, (B) the trigger
   to activate the menu, and (C) the content to show/hide when the trigger
   is clicked. So the markup looks something like:

   <div data-js-hook="behavior_flyout-menu">
     <button data-js-hook="behavior_flyout-menu_trigger">
     <div data-js-hook="behavior_flyout-menu_content">

   ========================================================================== */

'use strict';

// Required modules.
var standardType = require( './standard-type' );
var dataHook = require( '../../modules/util/data-hook' );


/**
 * @param {string} behaviorSelector
 *  Behavior type used to find the element within the dom.
 * @param {HTMLNode} baseElement Containing element for the behavior element.
 * @returns {HTMLNodeList} behaviorElements if it exists in the dom,
 *                         null otherwise.
 */
function _findElements( behaviorSelector, baseElement ) {
  baseElement = baseElement || document;
  var behaviorElements = [];

  try {
    behaviorElements = baseElement.querySelectorAll( behaviorSelector );
  } catch ( error ) {
    var msg = behaviorSelector + ' not found in DOM!';
    throw new Error( msg );
  }

  if ( behaviorElements.length === 0 &&
       behaviorSelector.indexOf( standardType.BEHAVIOR_PREFIX ) === -1 ) {
    behaviorElements = find( behaviorSelector, baseElement );
  }

  return behaviorElements;
}


/**
 * @param {( string|HTMLNode|HTMLNodeList )} behaviorElement
 *  Used to query dom for elements.
 * @param {string} event Event type to add to element.
 * @param {Function} eventHandler Callback for event.
 * @param {HTMLNode} baseElement Containing element for the behavior element.
 * @returns {HTMLNodeList} if it exists in the dom, null otherwise.
 */
function attach( behaviorElement, event, eventHandler, baseElement ) {
  var behaviorElements = [];

  if ( behaviorElement instanceof NodeList === true ) {
    behaviorElements = behaviorElement;
  } else if ( behaviorElement instanceof Node === true ) {
    behaviorElements = [ behaviorElement ];
  } else if ( typeof behaviorElement === 'string' ) {
    behaviorElements = _findElements( behaviorElement, baseElement );
  }

  for ( var i = 0, len = behaviorElements.length; i < len; i++ ) {
    behaviorElements[i].addEventListener( event, eventHandler, false );
  }

  return behaviorElements;
}

/**
 * @param {HTMLNode} element
 *   The DOM element within which to search for the behavior
 *   in the data-js-hook attribute.
 * @param {string} behaviorDataAttr
 *   The value in the data-js-hook. This is the name of the behavior.
 *   E.g. `behavior_flyout-menu`, `behavior_flyout-menu_content`.
 * @returns {HTMLNode} The DOM element that has an attached behavior.
 * @throws {Error} If data-js-hook attribute value was not found on DOM element.
 */
function checkBehaviorDom( element, behaviorDataAttr ) {
  // Check that the behavior is found on the passed DOM node.
  var dom;

  if ( dataHook.contains( element, behaviorDataAttr ) ) {
    dom = element;
    return dom;
  }

  // If the passed DOM node isn't null,
  // query the node to see if it's in the children.
  if ( element ) {
    var selector = '[' + standardType.JS_HOOK + '=' + behaviorDataAttr + ']';
    dom = element.querySelector( selector );
  }

  if ( !dom ) {
    var msg = behaviorDataAttr + ' behavior not found on passed DOM node!';
    throw new Error( msg );
  }

  return dom;
}

/**
 * @param {string} behaviorSelector
 *  Behavior type used to find the element within the dom.
 * @param {HTMLNode} baseElement Containing element for the behavior element.
 * @returns {HTMLNodeList} if it exists in the dom, null otherwise.
 */
function find( behaviorSelector, baseElement ) {
  behaviorSelector =
  standardType.JS_HOOK + '*=' + standardType.BEHAVIOR_PREFIX + behaviorSelector;
  behaviorSelector = '[' + behaviorSelector + ']';

  return _findElements( behaviorSelector, baseElement );
}

/**
 * @param {HTMLNode} behaviorElement Element in which to remove the event.
 * @param {string} event Event type to remove from the element.
 * @param {Function} eventHandler Callback for event.
 */
function remove( behaviorElement, event, eventHandler ) {
  behaviorElement.removeEventListener( event, eventHandler );
}

// Expose public methods.
module.exports = {
  attach: attach,
  checkBehaviorDom: checkBehaviorDom,
  find: find,
  remove: remove
};
