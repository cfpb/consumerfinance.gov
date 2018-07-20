/* ==========================================================================
   Scripts for Secondary Navigation organism
   ========================================================================== */

const dom = document.querySelector( '.o-secondary-navigation' );

/* Check that this script has been delivered to a page that actually
   has secondary navigation markup. */
if ( dom ) {
  require( 'cf-expandables' );
}
