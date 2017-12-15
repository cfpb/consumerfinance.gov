/* ==========================================================================
   Scripts for `/external-site/`.
   ========================================================================== */


const ExternalSite = require( '../../modules/ExternalSite.js' );
const externalSite = new ExternalSite( document.querySelector( '.external-site_container' ) );
externalSite.init();
