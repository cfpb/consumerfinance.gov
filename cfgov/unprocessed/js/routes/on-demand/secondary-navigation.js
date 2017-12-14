/* ==========================================================================
   Scripts for Secondary Navigation organism
   ========================================================================== */


const SecondaryNavigation = require( '../../organisms/SecondaryNavigation' );

const dom = document.querySelector( '.o-secondary-navigation' );

/* Check that this script has been delivered to a page that actually
   has secondary navigation markup. */
if ( dom ) {
  const secondaryNavigation = new SecondaryNavigation( dom ).init();
}
