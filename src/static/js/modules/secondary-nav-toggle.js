/* ==========================================================================
   Nav-secondary.
   This is for the sidenav on, e.g. /doing-business-with-us/past-awards/.
   ========================================================================== */

'use strict';
var View = require( './classes/View' );
var BreakpointHandler = require( './classes/BreakpointHandler' );
var getViewportDimensions = require( './util/get-viewport-dimensions' );

function init() {

  var breakpointHandler = new BreakpointHandler( {
    breakpoint: 599,
    type:       'max',
    enter:      _toggleNav,
    leave:      _toggleNav
  } );

  _toggleNav( getViewportDimensions.width );

}

function _toggleNav( width ) {
  var navExpandableView = View.getInstance( '.nav-secondary' );

  if ( !navExpandableView ) return;

  if ( width < 599 ) {
    navExpandableView.collapse( 0 );
  } else {
    navExpandableView.expand( 0 );
  }
}

// Expose public methods.
module.exports = { init: init };
