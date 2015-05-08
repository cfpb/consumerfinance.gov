/* ==========================================================================
   Footer Button: Scroll to Top
   ========================================================================== */

'use strict';

var $ = require( 'jquery' );

function init() {
  var duration = 300;

  $( '.js-return-to-top' ).click( function( event ) {
    event.preventDefault();
    $( 'html, body' ).animate( { scrollTop: 0 }, duration );
  } );
}

module.exports = { init: init };
