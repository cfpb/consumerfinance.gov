/* ==========================================================================
   Scripts for `/careers/working-at-cfpb/`.
   ========================================================================== */

'use strict';

var MobileCarousel = require( '../../../modules/classes/MobileCarousel' );

function init() {

  // TODO: Remove this when per-page JS is introduced.
  if ( document.querySelectorAll( '.careers-working-at-cfpb' ).length === 0 ) {
    return;
  }

  // MobileCarousel with 599px breakpoint.
  var mobileCarousel = new MobileCarousel( 599 );
  mobileCarousel.enableOn( '.js-mobile-carousel' );
}

module.exports = { init: init };
