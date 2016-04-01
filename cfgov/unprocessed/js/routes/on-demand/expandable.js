/* ==========================================================================
   Scripts for Expandable Molecule.
   ========================================================================== */

'use strict';

var atomicHelpers = require( '../../modules/util/atomic-helpers' );
var Expandable = require( '../../molecules/Expandable' );

atomicHelpers.instantiateAll( '.m-expandable', Expandable );
