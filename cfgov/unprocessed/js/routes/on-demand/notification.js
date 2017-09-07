/* ==========================================================================
   Scripts for Notification molecule.
   ========================================================================== */

'use strict';

const atomicHelpers = require( '../../modules/util/atomic-helpers' );
const Notification = require( '../../molecules/Notification' );

atomicHelpers.instantiateAll( '.m-notification', Notification );
