/* ==========================================================================
   Scripts for `/external-site/`.
   ========================================================================== */

import ExternalSite from '../modules/ExternalSite';
const externalSiteDom = document.querySelector(
  `.${ ExternalSite.BASE_CLASS }`
);
const externalSite = new ExternalSite( externalSiteDom );
externalSite.init();
