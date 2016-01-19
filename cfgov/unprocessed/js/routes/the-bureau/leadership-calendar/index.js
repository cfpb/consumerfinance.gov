/* ==========================================================================
   Leadership-calendar.
   Scripts for `/the-bureau/leadership-calendar/`.
   ========================================================================== */

'use strict';

// Required polyfills for <IE8.
require( '../../../modules/polyfill/query-selector' );

// List of organisms used.
var Expandable = require( '../../../molecules/Expandable' );
var expandables = document.querySelectorAll( '.m-expandable' );
var expandable;

for ( var i = 0, len = expandables.length; i < len; i++ ) {
  expandable = new Expandable( expandables[i] );
  expandable.init();
}
