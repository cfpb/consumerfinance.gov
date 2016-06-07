/* ==========================================================================
   Scripts for Expandable Molecule.
   ========================================================================== */

'use strict';

var atomicHelpers = require( '../../modules/util/atomic-helpers' );
var Expandable = require( '../../organisms/Expandable' );

atomicHelpers.instantiateAll( '.o-expandable', Expandable );
