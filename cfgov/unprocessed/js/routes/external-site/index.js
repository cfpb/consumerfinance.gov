/* ==========================================================================
   Bureau structure.
   Scripts for `/external-site/`.
   ========================================================================== */

'use strict';

var ExternalSite = require( '../../modules/ExternalSite.js' );
var externalSite = new ExternalSite( document.querySelector( '.external-site_container' ) );
externalSite.init();
