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


/*'use strict';

var $ = require( 'jquery' );

function init() {
  $( '.js-return-to-top' ).click( function( event ) {
    event.preventDefault();
    returnToTop(300);
  } );
}

function returnToTop(duration) {
  $( 'html, body' ).animate( { scrollTop: 0 }, duration );
}

module.exports = { init: init };*/
