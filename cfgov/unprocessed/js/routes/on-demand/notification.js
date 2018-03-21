/* ==========================================================================
   Scripts for Notification molecule.
   ========================================================================== */


const atomicHelpers = require( '../../modules/util/atomic-helpers' );
const Notification = require( '../../molecules/Notification' );

atomicHelpers.instantiateAll( '.m-notification', Notification );
