/* ==========================================================================
   Bureau structure.
   Scripts for `/the-bureau/`.
   ========================================================================== */

'use strict';

var $ = require( 'jquery' );
var MobileCarousel = require( '../../modules/classes/MobileCarousel' );
var MobileOnlyExpandable =
  require( '../../modules/classes/MobileOnlyExpandable' );


function init() {

  // TODO: Remove this when per-page JS is introduced.
  if ( document.querySelectorAll( '.the-bureau' ).length === 0 ) {
    return;
  }

  var mobileCarousel = new MobileCarousel();
  mobileCarousel.enableOn( '.js-mobile-carousel' );

  $( '.expandable__mobile-only' ).each( function() {
    new MobileOnlyExpandable( $( this ) ); // eslint-disable-line no-new, no-inline-comments, max-len
  } );
}

module.exports = { init: init };
