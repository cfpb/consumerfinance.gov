/* ==========================================================================
   Bureau structure.
   Scripts for `/the-bureau/`.
   ========================================================================== */

'use strict';

var $ = require( 'jquery' );
var MobileCarousel = require( '../../modules/classes/MobileCarousel' );
var MobileOnlyExpandable = require( '../../modules/classes/MobileOnlyExpandable' );

function init() {

  // TODO: Remove this when per-page JS is introduced.
  if ( document.querySelectorAll( '.the-bureau' ).length === 0 ) {
    return;
  }

  // MobileCarousel with 599px breakpoint.
  var mobileCarousel = new MobileCarousel( 599 );
  mobileCarousel.enableOn( '.js-mobile-carousel' );

  $( '.expandable__mobile-only' ).each( function() {
    new MobileOnlyExpandable( $( this ), breakpointPx ); // eslint-disable-line
  } );
}

module.exports = { init: init };
