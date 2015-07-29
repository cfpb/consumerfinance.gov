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

  var breakpointPx = 599;

  $( '.expandable__mobile-only' ).each( function() {
    // ESLint no-new rule ignored
    new MobileOnlyExpandable( $( this ), breakpointPx ); // eslint-disable-line
  } );
}

module.exports = { init: init };
