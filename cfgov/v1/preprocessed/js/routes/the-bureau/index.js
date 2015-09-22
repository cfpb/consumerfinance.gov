/* ==========================================================================
   Bureau structure.
   Scripts for `/the-bureau/`.
   ========================================================================== */

'use strict';

require( '../../modules/init-mobile-only-expandables' ).init();

var MobileCarousel = require( '../../modules/classes/MobileCarousel' );
var mobileCarousel = new MobileCarousel();
mobileCarousel.enableOn( '.js-mobile-carousel' );
