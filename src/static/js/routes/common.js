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
require( '../modules/nav-primary.js' ).init();
require( '../modules/secondary-nav-toggle' ).init();
require( '../modules/footer-button' ).init();
require( '../modules/focus-target' ).init();
require( '../modules/post-filter' ).init();
require( '../modules/init-chosen' ).init();
require( '../modules/form-validation' ).init();
require( '../modules/reveal-on-focus' ).init();
require( '../modules/scroll-on-history-collapse' ).init();
require( '../modules/clear-form-buttons' ).init();
require( '../modules/jquery/custom-input' ).init();
require( '../modules/jquery/custom-select' ).init();
require( '../modules/youtube' ).init();
require( '../modules/pagination-validation.js' ).init();
require( '../modules/show-hide-fields.js' ).init();
require( '../modules/external-site-redirect.js' ).init();
