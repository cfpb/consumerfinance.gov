/* ==========================================================================
   Scripts for Secondary Navigation organism
   ========================================================================== */

'use strict';

var SecondaryNavigation = require( '../../organisms/SecondaryNavigation' );

var dom = document.querySelector( '.o-secondary-navigation' );
// Check that this script has been delivered to a page that actually
// has secondary navigation markup.
if ( dom ) {
  var secondaryNavigation = new SecondaryNavigation( dom ).init();
}
