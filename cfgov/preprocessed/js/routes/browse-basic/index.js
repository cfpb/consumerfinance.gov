/* ==========================================================================
   Scripts for /browse-basic/.
   ========================================================================== */

'use strict';

// List of organisms used.
var ExpandableGroup = require( '../../organisms/ExpandableGroup' );

var expandables = document.querySelectorAll( '.expandable-group' );

var regularExpandableGroup = new ExpandableGroup( expandables[0] );
var accordionExpandableGroup = new ExpandableGroup( expandables[1] );

regularExpandableGroup.init();
accordionExpandableGroup.init();
