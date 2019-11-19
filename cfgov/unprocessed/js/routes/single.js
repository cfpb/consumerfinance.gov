/* ==========================================================================
   Scripts for the hompage only.
   ========================================================================== */

import Carousel from '../organisms/Carousel.js';

const carouselDom = document.querySelector( `.${ Carousel.BASE_CLASS }` );
const carousel = new Carousel( carouselDom );
carousel.init();
