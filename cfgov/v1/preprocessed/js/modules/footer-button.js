/* ==========================================================================
   Footer Button: Scroll to Top
   ========================================================================== */

'use strict';

var $ = require( 'jquery' );

/**
 * Set up event handler for button to scroll to top of page.
 */
function init() {
  var duration = 300;

  $( '.js-return-to-top' ).click( function( event ) {
    event.preventDefault();
    $( 'html, body' ).animate( { scrollTop: 0 }, duration );
  } );
}

module.exports = { init: init };
