/* ==========================================================================
   Initialization script for Featured Content Module.
   ========================================================================== */

import FeaturedContentModule from '../../organisms/FeaturedContentModule';

const featuredContentModuleDom = document.querySelector(
  `.${ FeaturedContentModule.BASE_CLASS }`
);
const featuredContentModule = new FeaturedContentModule(
  featuredContentModuleDom
);
featuredContentModule.init();
