/* ==========================================================================
   Reveal on focus
   ========================================================================== */

'use strict';

var $ = require( 'jquery' );

function init() {
  $( '.reveal-on-focus' )
    .find( '.reveal-on-focus_content' ).hide()
    .end()
    .find( '.reveal-on-focus_target' ).on( 'focus', function() {
      $( this )
        .parents( '.reveal-on-focus' )
        .find( '.reveal-on-focus_content' ).slideDown();
    } );
}

module.exports = { init: init };
