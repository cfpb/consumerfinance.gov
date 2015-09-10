/* ==========================================================================
   Scripts for `/careers/working-at-cfpb/`.
   ========================================================================== */

'use strict';

var breakpointsConfig = require( '../../../config/breakpoints-config' );
var MobileCarousel = require( '../../../modules/classes/MobileCarousel' );

var mobileCarousel = new MobileCarousel( breakpointsConfig.mobile.max );
mobileCarousel.enableOn( '.js-mobile-carousel' );
