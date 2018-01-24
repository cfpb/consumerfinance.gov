/* ==========================================================================
   Common application-wide scripts that are used across the whole site.
   ========================================================================== */

// Global modules.
require( '../modules/focus-target' ).init();

// GLOBAL ATOMIC ELEMENTS.

// Organisms.
const Header = require( '../organisms/Header.js' );
const header = new Header( document.body );
// Initialize header by passing it reference to global overlay atom.
header.init( document.body.querySelector( '.a-overlay' ) );

const Footer = require( '../organisms/Footer.js' );
const footer = new Footer( document.body ).init();
