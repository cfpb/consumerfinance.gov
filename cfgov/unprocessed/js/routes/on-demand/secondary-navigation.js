/* ==========================================================================
   Scripts for Secondary Navigation organism
   ========================================================================== */

'use strict';

var SecondaryNavigation = require( '../../organisms/SecondaryNavigation' );

var dom = document.querySelector( '.content_sidebar .o-secondary-navigation' );
var secondaryNavigation = new SecondaryNavigation( dom ).init();
