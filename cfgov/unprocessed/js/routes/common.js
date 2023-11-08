/* ==========================================================================
   Common application-wide scripts that are used across the whole site.
   ========================================================================== */

// GLOBAL ATOMIC ELEMENTS.

// Organisms.
import { Footer } from '../organisms/Footer.js';
import { Header } from '../organisms/Header.js';

const header = new Header(document.body);
// Initialize header by passing it reference to global overlay atom.
header.init(document.body.querySelector('.a-overlay'));

Footer.init(document.body);
