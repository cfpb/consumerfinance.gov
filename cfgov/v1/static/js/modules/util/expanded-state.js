/* ==========================================================================
   Expanded State Utils
   ========================================================================== */

'use strict';

var $ = require( 'jquery' );
var navTimeOut;

/**
 * @returns {Boolean}      True if element's aria-expanded value equals "true"
 * @param  {object}  $elem Element to test
 */
function isThisExpanded( $elem ) {
  return $elem.attr( 'aria-expanded' ) === 'true';
}

/**
 * Check if at least one element has a value of "true" set to an
 * aria-expanded attr
 *
 * @returns {Boolean}        True if at least one elements' aria-expanded value
 *                          equals "true"
 * @param  {object}  $elems Elements to test
 */
function isOneExpanded( $elems ) {
  var oneExpanded = false;

  $elems.each( function() {
    if ( isThisExpanded( $( this ) ) ) {
      oneExpanded = true;
    }
  } );

  return oneExpanded;
}

/**
 * Change the value of the element's aria-expanded attribute based on it's
 * current state if one is not passed. Allows for a delayed event for
 * animated elements
 * @param  {object}   $elem The element to change the aria-expanded attr of
 * @param  {string}   state The value, if any, to set the aria-expanded attr
 *                          to. Options are "true", "false" or null
 * @param  {Function} cb    The function to execute after a delay
 * @param  {integer}  delay The length of time to delay the execution of the
 *                          passed callback
 */
function toggleExpandedState( $elem, state, cb, delay ) {
  delay = delay || 300;
  state = state || !isThisExpanded( $elem );
  clearTimeout( navTimeOut );

  $elem.attr( 'aria-expanded', state );

  if ( cb ) {
    navTimeOut = setTimeout( function() {
      return cb();
    }, delay );
  }
}

module.exports = {
  get: {
    isThisExpanded: isThisExpanded,
    isOneExpanded:  isOneExpanded
  },
  set: {
    toggleExpandedState: toggleExpandedState
  }
};
