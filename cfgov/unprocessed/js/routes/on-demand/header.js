/* ==========================================================================
   Scripts for Expandable Group organism.
   ========================================================================== */

'use strict';

// GLOBAL ATOMIC ELEMENTS.
// Organisms.
var Header = require( '../../organisms/Header.js' );
var header = new Header( document.body );
// Initialize header by passing it reference to global overlay atom.
header.init( document.body.querySelector( '.a-overlay' ) );
