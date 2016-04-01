/* ==========================================================================
   Scripts for Filterable List Controls organism
   ========================================================================== */

'use strict';

var atomicHelpers = require( '../../modules/util/atomic-helpers' );
var FilterableListControls = require( '../../organisms/FilterableListControls' );

atomicHelpers.instantiateAll( '.o-filterable-list-controls', FilterableListControls );
