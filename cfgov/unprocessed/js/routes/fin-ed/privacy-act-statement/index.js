/* ==========================================================================
   Scripts for `/fin-ed/privacy-act-statement/.
   ========================================================================== */

const dom = document.querySelector( '.o-secondary-navigation' );

/* Check that this script has been delivered to a page that actually
   has secondary navigation markup. */
if ( dom ) {
  // eslint-disable-next-line global-require
  require( 'cf-expandables' );
}

