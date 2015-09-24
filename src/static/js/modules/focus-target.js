/* ==========================================================================
   Focus Target

   This is necessary because of a webkit quirk with handling keyboard
   focus with anchor links. It'll mostly be used on the skip nav link.

   If that webkit bug is fixed, remove this JS.

========================================================================== */

'use strict';

var $ = require( 'jquery' );

/**
 * Parse links to handle webkit bug with keyboard focus.
 */
function init() {
  $( 'a[href^="#"]' ).click( function() {
    var anchor = $( this ).attr( 'href' );
    $( anchor ).attr( 'tabindex', -1 ).focus();
  } );
}

module.exports = { init: init };
