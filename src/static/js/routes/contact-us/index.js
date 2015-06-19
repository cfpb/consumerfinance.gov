/* ==========================================================================
   Contact us
   Scripts for /contact-us/.
   ========================================================================== */

'use strict';

var $ = require( 'jquery' );
require( '../../modules/jquery/type-and-filter' ).init();

function init() {
  // Initialize contact us filtering.
  $( '.type-and-filter' ).typeAndFilter( {
    $input:                  $( '.js-type-and-filter_input' ),
    $items:                  $( '.js-type-and-filter_item' ),
    $form:                   $( '.js-type-and-filter_form' ),
    $clear:                  $( '.js-type-and-filter_clear' ),
    allMessage:              'Showing all {{ count }} contacts.',
    filteredMessageSingular: '{{ count }} filtered contact result.',
    filteredMessageMultiple: '{{ count }} filtered contact results.'
  } );

  // Hide the contact list header if there are zero results.
  $( '.type-and-filter' ).on( 'attemptSearch', function() {
    var resultsCount = $( '.js-type-and-filter_item' ).filter( ':visible' ).length;
    $( '#contact-list_header' ).toggle( resultsCount > 0 );
  } );

  // Clicking on a helpful term should trigger a filter.
  $( '.js-helpful-term' ).on( 'click', function() {
    $( '.js-type-and-filter_input' ).val( $( this ).text() ).trigger( 'valChange' );
  } );
}

module.exports = { init: init };
