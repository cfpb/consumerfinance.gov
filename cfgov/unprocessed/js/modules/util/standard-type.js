/**
 * @constant
 * @type {string}
 * @description
 * Constant for the name of the data-* attribute set on
 * HTML DOM elements for access by JavaScript.
 */
const JS_HOOK = 'data-js-hook';

/**
 * @constant
 * @type {string}
 * @description
 * Flag prefix for settings that describe what JavaScript
 * behaviors should be attached to a component.
 * This would be set in the markup and initialized when
 * the JavaScript loads.
 *
 * @example
 * A component may flag that it has certain JavaScript behaviors attached,
 * such as:
 * `data-js-hook="behavior_flyout-menu behavior_clearable-input"`,
 * which defines that two scripts (FlyoutMenu) and (ClearableInput)
 * should access this DOM element and initialize its behaviors.
 */
const BEHAVIOR_PREFIX = 'behavior_';

/**
 * @constant
 * @type {string}
 * @description
 * Flag prefix for settings related to changes in a components
 * state set in the data-* JavaScript hook.
 *
 * @example
 * A component may flag that it has been initialized by setting
 * `data-js-hook="state_atomic_init"` after page load.
 * Which specifies that the init method of a atomic constructor
 * has been called, such as
 * `var globalSearch = new GlobalSearch( 'm-global-search' ).init()`.
 */
const STATE_PREFIX = 'state_';

/**
 * Empty function that will do nothing.
 * A usecase is when an object has empty functions used for callbacks,
 * which are meant to be overridden with functionality, but if not,
 * noopFunct will fire and do nothing instead.
 *
 * @example
 * callback.onComplete = standardType.noopFunct;
 */
function noopFunct() {
  // Placeholder function meant to be overridden.
}

let UNDEFINED;

module.exports = {
  BEHAVIOR_PREFIX: BEHAVIOR_PREFIX,
  JS_HOOK:         JS_HOOK,
  noopFunct:       noopFunct,
  STATE_PREFIX:    STATE_PREFIX,
  UNDEFINED:       UNDEFINED
};
