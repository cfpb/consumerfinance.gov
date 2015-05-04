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
  require( '../modules/alert' ).init();
  require( '../modules/beta-banner-state' ).init();
  require( '../modules/secondary-nav-toggle' ).init();
  require( '../modules/post-filters-form-validation' ).init();
  require( '../modules/init-chosen' ).init();
  require( '../modules/slide-push-menu' ).init();
  require( '../modules/form-validation' ).init();
  require( '../modules/reveal-on-focus' ).init();
  require( '../modules/desktop-menu-transitions' ).init();
  require( '../modules/scroll-on-history-collapse' ).init();
  require( '../modules/clear-form-buttons' ).init();
  require( '../modules/jquery/cf_pagination' ).init();
  require( '../modules/jquery/custom-input' ).init();
  require( '../modules/jquery/custom-select' ).init();

  // Page-specifc modules.
  require( './blog/index.js' );
  require( './contact-us/index.js' );
  require( './index.js' );
  require( './the-bureau/index.js' );
  require( './the-bureau/bureau-structure/index.js' );
} );
