/* ==========================================================================
   Nav-secondary.
   This is for the sidenav on, e.g. /doing-business-with-us/past-awards/.
   ========================================================================== */

'use strict';

var $ = require( 'jquery' );

function init() {
  // Call this right away to test if we need to expand the nav.
  _navSecondaryToggle();

  // Then on window resize check to see when we need to toggle the nav.
  $( window ).resize( function() {
    _navSecondaryToggle();
  } );
}

function _navSecondaryToggle() {
  if ( _navSecondaryToggleTest() ) {
    $( '.nav-secondary .expandable_target' ).trigger( 'click' );
  }
}

// Tests whether or not the secondary nav should be toggled.
function _navSecondaryToggleTest() {
  var isSmall = $( '.nav-secondary .nav-secondary_link__button' ).is( ':visible' ),
    isExpanded = $( '.nav-secondary .expandable_content' ).attr( 'aria-expanded' ) === 'true';
  return isSmall && isExpanded || !isSmall && !isExpanded;
}

// Expose public methods.
module.exports = { init: init };
