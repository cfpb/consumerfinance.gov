/* ==========================================================================
   Scripts for Secondary Navigation organism
   ========================================================================== */

'use strict';

var SecondaryNavigation = require( '../../organisms/SecondaryNavigation' );

var dom = document.querySelector( '.o-secondary-navigation' );
var secondaryNavigation = new SecondaryNavigation( dom ).init();
