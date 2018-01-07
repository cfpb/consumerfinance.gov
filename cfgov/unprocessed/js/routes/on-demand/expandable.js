/* ==========================================================================
   Scripts for Expandable Molecule.
   ========================================================================== */


const atomicHelpers = require( '../../modules/util/atomic-helpers' );
const Expandable = require( '../../organisms/Expandable' );

atomicHelpers.instantiateAll( '.o-expandable', Expandable );
