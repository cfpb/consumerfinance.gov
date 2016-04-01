/* ==========================================================================
   Nav-secondary.
   This is for the sidenav on,e.g./about-us/doing-business-with-us/past-awards/.
   ========================================================================== */

'use strict';

var $ = require( 'jquery' );
var getBreakpointState = require( './util/breakpoint-state' ).get;

/**
 * Check if nav needs to be toggled or not, on load and window resize.
 */
function init() {
  // Call this right away to test if we need to expand the nav.
  _navSecondaryToggle();

  // Then on window resize check to see when we need to toggle the nav.
  $( window ).resize( function() {
    _navSecondaryToggle();
  } );
}

/**
 * Trigger a click on the secondary nav.
 */
function _navSecondaryToggle() {
  if ( _navSecondaryToggleTest() ) {
    $( '.o-secondary-navigation .expandable_target' ).trigger( 'click' );
  }
}

/**
 * @returns {boolean} True if mobile state and expanded
 *   or desktop size and not expanded, false otherwise.
 */
function _navSecondaryToggleTest() {
  var breakpointState = getBreakpointState();
  var isSmall = breakpointState.isBpXS || breakpointState.isBpSM;

  var isExpanded =
    $( '.o-secondary-navigation .expandable_content' )
      .attr( 'aria-expanded' ) === 'true';
  return isSmall && isExpanded || !isSmall && !isExpanded;
}

// Expose public methods.
module.exports = { init: init };
