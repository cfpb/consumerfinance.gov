/* ==========================================================================
   Common application-wide scripts that are used across the whole site.
   ========================================================================== */

'use strict';

var $ = require( 'jquery' );

$( document ).ready( function() {

  // Shimmed-Browserify modules (other than jQuery).
  require( 'jquery-easing' );
  require( 'cf-expandables' );

  // Native-Browserify modules.
  require( '../modules/beta-banner-state' ).init();
  require( '../modules/secondary-nav-toggle' ).init();
  require( '../modules/post-filter' ).init();
  require( '../modules/init-chosen' ).init();
  require( '../modules/mobile-primary-nav.js' ).init();
  require( '../modules/desktop-primary-nav.js' ).init();
  require( '../modules/form-validation' ).init();
  require( '../modules/reveal-on-focus' ).init();
  require( '../modules/scroll-on-history-collapse' ).init();
  require( '../modules/clear-form-buttons' ).init();
  require( '../modules/jquery/cf_pagination' ).init();
  require( '../modules/jquery/custom-input' ).init();
  require( '../modules/jquery/custom-select' ).init();
  require( '../modules/footer-button' ).init();
  require( '../modules/youtube' ).init();
  require( '../modules/pagination-validation.js' ).init();
  require( '../modules/show-hide-fields.js' ).init();
  require( '../modules/external-site.js' ).init();
  require( '../modules/external-site-redirect.js' ).init();

  // Page-specific modules.
  require( './contact-us/index.js' ).init();
  require( './index.js' ).init();
  require( './careers/working-at-cfpb/index.js' ).init();
  require( './careers/current-openings/index.js' ).init();
  require( './careers/application-process/index.js' ).init();
  require( './the-bureau/index.js' ).init();
  require( './the-bureau/bureau-structure/index.js' ).init();
  require( './offices/index.js' ).init();
} );
