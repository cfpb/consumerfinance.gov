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

// Expose public methods.
module.exports = {
  checkBehaviorDom: checkBehaviorDom
};
