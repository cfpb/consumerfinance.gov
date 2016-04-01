/* ==========================================================================
   Scripts for Expandable Group organism.
   ========================================================================== */

'use strict';

var atomicHelpers = require( '../../modules/util/atomic-helpers' );
var ExpandableGroup = require( '../../organisms/ExpandableGroup' );

atomicHelpers.instantiateAll( '.o-expandable-group', ExpandableGroup );
