/* ==========================================================================
   Scripts for /browse-basic/.
   ========================================================================== */

'use strict';

// List of organisms used.
var Expandable = require( '../../molecules/Expandable' );
var ExpandableGroup = require( '../../organisms/ExpandableGroup' );

var selector = '.expandable-prototypes .m-expandable';
var expandables = document.querySelectorAll( selector );

var expandable;
for ( var i = 0, len = expandables.length; i < len; i++ ) {
  expandable = new Expandable( expandables[i] );
  expandable.init();
}

selector = '.expandable-group-prototypes .o-expandable-group';
var expandableGroup = document.querySelectorAll( selector );
var regularExpandableGroup = new ExpandableGroup( expandableGroup[0] );

regularExpandableGroup.init();
