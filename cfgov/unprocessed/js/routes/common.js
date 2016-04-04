/* ==========================================================================
   Common application-wide scripts that are used across the whole site.
   ========================================================================== */

'use strict';

// Vendor libraries.
require( 'jquery' );
require( 'jquery-easing' );
require( 'cf-expandables' );

// Global modules.
require( '../modules/footer-button' ).init();
require( '../modules/focus-target' ).init();
require( '../modules/form-validation' ).init();
require( '../modules/clear-form-buttons' ).init();
require( '../modules/UStreamPlayer' ).init( '.video-player__ustream' );
require( '../modules/YoutubePlayer' ).init( '.video-player__youtube' );
require( '../modules/pagination-validation.js' ).init();

// GLOBAL ATOMIC ELEMENTS.
// Organisms.
var Header = require( '../organisms/Header.js' );
var header = new Header( document.body );
// Initialize header by passing it reference to global overlay atom.
header.init( document.body.querySelector( '.a-overlay' ) );

// Multi-select.
// TODO: Move to browse-filterable route after old WP pages are removed
var Multiselect = require( '../molecules/Multiselect' );
var selects = document.querySelectorAll( 'select[multiple]' );

var multiselect;
for ( var i = 0, len = selects.length; i < len; i++ ) {
  multiselect = new Multiselect( selects[i] );
  multiselect.init();
}
