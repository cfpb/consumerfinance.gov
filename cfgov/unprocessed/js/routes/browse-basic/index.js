/* ==========================================================================
   Scripts for /browse-basic/.
   ========================================================================== */

'use strict';

// Required polyfills for <IE8.
require( '../../modules/polyfill/query-selector' );

// List of organisms used.
var Expandable = require( '../../molecules/Expandable' );
var ExpandableGroup = require( '../../organisms/ExpandableGroup' );

var expandables = document.querySelectorAll( '.expandable-prototypes .m-expandable' );

var expandable;
for ( var i = 0, len = expandables.length; i < len; i++ ) {
  expandable = new Expandable( expandables[i] ).init();
}

var expandableGroup = document.querySelectorAll( '.expandable-group-prototypes .o-expandable-group' );
var regularExpandableGroup = new ExpandableGroup( expandableGroup[0] );
var accordionExpandableGroup = new ExpandableGroup( expandableGroup[1] );

regularExpandableGroup.init();
accordionExpandableGroup.init();
