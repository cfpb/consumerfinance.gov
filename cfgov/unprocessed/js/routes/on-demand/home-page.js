/* ==========================================================================
   Scripts for the homepage only.
   ========================================================================== */

import Carousel from '../../organisms/Carousel.js';

const carouselDom = document.querySelector( `.${ Carousel.BASE_CLASS }` );

if ( carouselDom ) {
  const carousel = new Carousel( carouselDom );
  carousel.init();
}
