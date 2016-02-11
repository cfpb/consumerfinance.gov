/* ==========================================================================
   Scripts for /learn-page/.
   ========================================================================== */

'use strict';

// List of organisms used.
var Expandable = require( '../../molecules/Expandable' );

var selector = '.m-expandable';
var expandables = document.querySelectorAll( selector );

var expandable;
for ( var i = 0, len = expandables.length; i < len; i++ ) {
  expandable = new Expandable( expandables[i] );
  expandable.init();
}
