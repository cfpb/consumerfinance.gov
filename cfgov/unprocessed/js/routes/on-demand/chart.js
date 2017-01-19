/* ==========================================================================
   Scripts for Line Chart molecule.
   ========================================================================== */

'use strict';

var atomicHelpers = require( '../../modules/util/atomic-helpers' );
var Chart = require( 'cfpb-chart-builder' );

atomicHelpers.instantiateAll( '.o-chart', Chart );
