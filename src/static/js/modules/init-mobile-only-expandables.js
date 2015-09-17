/* ==========================================================================
   Initialize use of mobile-only expandable.
   ========================================================================== */

'use strict';

var $ = require( 'jquery' );
var MobileOnlyExpandable =
  require( './classes/MobileOnlyExpandable' );

function init() {
  $( '.expandable__mobile-only' ).each( function() {
    new MobileOnlyExpandable( $( this ) ); // eslint-disable-line no-new, no-inline-comments, max-len
  } );
}

module.exports = { init: init };
