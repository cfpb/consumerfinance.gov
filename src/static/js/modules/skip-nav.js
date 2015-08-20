/* ==========================================================================
   Skip Nav

   This is necessary because of a webkit quirk with handling keyboard
   focus with anchor links. If that webkit bug is fixed, remove this JS.

========================================================================== */

'use strict';

var $ = require( 'jquery' );

function init() {
  $( 'a[href^="#"]' ).click( function() {
    var anchor = $(this).attr( 'href' );
    $( anchor ).attr( 'tabindex', -1 ).focus();
  } );
}

module.exports = { init: init };
