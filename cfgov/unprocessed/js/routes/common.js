/* ==========================================================================
   Common application-wide scripts that are used across the whole site.
   ========================================================================== */

'use strict';

// Vendor libraries.
require( 'jquery' );
require( 'jquery-easing' );
require( 'cf-expandables' );

// Global modules.
require( '../modules/beta-banner-state' ).init();
require( '../modules/footer-button' ).init();
require( '../modules/focus-target' ).init();
require( '../modules/post-filter' ).init();
require( '../modules/init-chosen' ).init();
require( '../modules/form-validation' ).init();
require( '../modules/scroll-on-history-collapse' ).init();
require( '../modules/clear-form-buttons' ).init();
require( '../modules/youtube' ).init();
require( '../modules/pagination-validation.js' ).init();
require( '../modules/show-hide-fields.js' ).init();
require( '../modules/external-site-redirect.js' ).init();

// GLOBAL ATOMIC ELEMENTS.
// Organisms.
var Header = require( '../organisms/Header.js' );
var header = new Header( document.body );
header.init();

// Secondary Navigation
var SecondaryNavigation = require( '../organisms/SecondaryNavigation' );
var secondaryNavigation = new SecondaryNavigation( document.body ).init();
