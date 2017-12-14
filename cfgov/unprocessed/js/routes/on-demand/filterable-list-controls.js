/* ==========================================================================
   Scripts for Filterable List Controls organism
   ========================================================================== */


const atomicHelpers = require( '../../modules/util/atomic-helpers' );
const FilterableListControls = require( '../../organisms/FilterableListControls' );

atomicHelpers.instantiateAll( '.o-filterable-list-controls', FilterableListControls );
