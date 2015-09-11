/* ==========================================================================
   Scripts for `/offices/`.
   ========================================================================== */

'use strict';

var $ = require( 'jquery' );
var MobileOnlyExpandable =
  require( '../../modules/classes/MobileOnlyExpandable' );

function init() {

  // TODO: Remove this when per-page JS is introduced.
  if ( document.querySelectorAll( '.office' ).length === 0 ) {
    return;
  }

  $( '.expandable__mobile-only' ).each( function() {
    new MobileOnlyExpandable( $( this ) ); // eslint-disable-line no-new, no-inline-comments, max-len
  } );
}

module.exports = { init: init };
