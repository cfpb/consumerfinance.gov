/* ==========================================================================
   Scripts for `/careers/application-process/.
   ========================================================================== */

'use strict';

var $ = require( 'jquery' );
var MobileOnlyExpandable = require( '../../../modules/classes/MobileOnlyExpandable' );

function init() {

  // TODO: Remove this when per-page JS is introduced.
  if ( document.querySelectorAll( '.careers-application-process' ).length === 0 ) {
    return;
  }

  $( '.expandable__mobile-only' ).each( function() {
    new MobileOnlyExpandable( $( this ), 599 ); // eslint-disable-line
  } );
}

module.exports = { init: init };
