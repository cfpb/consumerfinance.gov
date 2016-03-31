/* ==========================================================================
   Scripts for Notification molecule.
   ========================================================================== */

'use strict';

var atomicHelpers = require( '../../modules/util/atomic-helpers' );
var ExpandableGroup = require( '../../molecules/Notification' );

atomicHelpers.instantiateAll( '.m-notification', Notification );
