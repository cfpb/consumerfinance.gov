/* ==========================================================================
   Footer Button: Scroll to Top
   ========================================================================== */
'use strict';

var $ = require( 'jquery' );

// TODO: Refactor this file to remove jquery dependency.
//       http://stackoverflow.com/questions/21474678/
//       scrolltop-animation-without-jquery
/**
 * Set up event handler for button to scroll to top of page.
 */
/* istanbul ignore next */
function init() {
  var duration = 300;

  // Disable Google Tag Manager tracking on this link.
  $( '.js-return-to-top' ).attr( 'data-gtm_ignore', 'true' );

  $( '.js-return-to-top' ).click( function( event ) {
    event.preventDefault();
    $( 'html, body' ).animate( { scrollTop: 0 }, duration );
  } );
}

module.exports = { init: init };
