/* ==========================================================================
   Common application-wide scripts that are used across the whole site.
   ========================================================================== */

'use strict';

// Vendor libraries.
require( 'jquery' );

// Global modules.
require( '../modules/focus-target' ).init();
require( '../modules/UStreamPlayer' ).init( '.video-player__ustream' );
require( '../modules/YoutubePlayer' ).init( '.video-player__youtube' );

// GLOBAL ATOMIC ELEMENTS.
// Organisms.
var Header = require( '../organisms/Header.js' );
var header = new Header( document.body );
// Initialize header by passing it reference to global overlay atom.
header.init( document.body.querySelector( '.a-overlay' ) );

var Footer = require( '../organisms/Footer.js' );
var footer = new Footer( document.body ).init();
