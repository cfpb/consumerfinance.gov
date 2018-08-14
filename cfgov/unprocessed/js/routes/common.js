/* ==========================================================================
   Common application-wide scripts that are used across the whole site.
   ========================================================================== */

// GLOBAL ATOMIC ELEMENTS.

// Organisms.
const Header = require( '../organisms/Header.js' );
const header = new Header( document.body );
// Initialize header by passing it reference to global overlay atom.
header.init( document.body.querySelector( '.a-overlay' ) );

const Footer = require( '../organisms/Footer.js' );
const footer = new Footer( document.body );
footer.init();

// Enable improved "Skip to Main Content" links
const SkipNav = require( '../modules/SkipNav.js' )();
