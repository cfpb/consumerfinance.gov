/* ==========================================================================
   Scripts for Expandable Group organism.
   ========================================================================== */


const atomicHelpers = require( '../../modules/util/atomic-helpers' );
const ExpandableGroup = require( '../../organisms/ExpandableGroup' );

atomicHelpers.instantiateAll( '.o-expandable-group', ExpandableGroup );
