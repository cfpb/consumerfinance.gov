/* ==========================================================================
   Scripts for Secondary Navigation organism
   ========================================================================== */
import Expandable from '@cfpb/cfpb-expandables/src/Expandable';

const dom = document.querySelector( '.o-secondary-navigation' );

/* Check that this script has been delivered to a page that actually
   has secondary navigation markup. */
if ( dom ) {
  Expandable.init( dom );
}
