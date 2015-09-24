/* ==========================================================================
   History: Scroll up when collapsing History sectons
   ========================================================================== */

'use strict';

var $ = require( 'jquery' );

/**
 * Set up DOM references and event handlers
 * for scrolling up when collapsing history sections.
 */
function init() {
  var $historySectionExpandable = $( '.history-section-expandable' );
  $historySectionExpandable.find( '.expandable_target' )
  .not( $historySectionExpandable.find( '.expandable .expandable_target' ) )
  .on( 'click', function() {
    if ( $( this ).attr( 'aria-pressed' ) === 'false' ) {
      $( 'html, body' ).animate( {
        scrollTop: $( this ).parent().offset().top - 15
      }, 500, 'easeOutExpo' );
    }
  } );
}

// Expose public methods.
module.exports = { init: init };
