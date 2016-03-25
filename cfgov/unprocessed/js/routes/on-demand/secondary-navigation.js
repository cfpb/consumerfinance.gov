/* ==========================================================================
   Scripts for Secondary Navigation Organism
   ========================================================================== */

'use strict';

// List of organisms used.
var SecondaryNavigation = require( '../../organisms/SecondaryNavigation' );
var secondaryNavigation = new SecondaryNavigation( document.querySelector( '.content_sidebar .o-secondary-navigation' ) ).init();