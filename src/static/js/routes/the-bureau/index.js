/* ==========================================================================
   Bureau structure.
   Scripts for `/the-bureau/`.
   ========================================================================== */

'use strict';

var MobileCarousel = require( '../../modules/classes/MobileCarousel' );

function init() {

  // TODO: Remove this when per-page JS is introduced.
  if ( document.querySelectorAll( '.the-bureau' ).length === 0 ) {
    return;
  }

  var mobileCarousel = new MobileCarousel();
  mobileCarousel.enableOn( '.js-mobile-carousel' );
}

module.exports = { init: init };
