'use strict';

// Constant for the name of the JS hook used
// for attaching JS behavior to HTML DOM elements.
var JS_HOOK = 'data-js-hook';

/**
 * Empty function that will do nothing.
 * A usecase is when an object has empty functions used for callbacks,
 * which are meant to be overridden with functionality, but if not,
 * noopFunct will fire and do nothing instead.
 *
 * e.g.
 * callback.onComplete = standardType.noopFunct;
 */
function noopFunct() {
  // Placeholder function meant to be overridden.
}

module.exports = {
  JS_HOOK:   JS_HOOK,
  noopFunct: noopFunct
};
