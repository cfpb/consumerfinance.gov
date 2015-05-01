/* ==========================================================================
   Contact us
   Scripts for /contact-us/.
   ========================================================================== */

'use strict';

require( '../../modules/jquery/type-and-filter' ).init();
var $ = require( 'jquery' );

// Initialize contact us filtering.
$( '.type-and-filter' ).typeAndFilter( {
  $input:                  $( '.js-type-and-filter_input' ),
  $items:                  $( '.js-type-and-filter_item' ),
  $button:                 $( '.js-type-and-filter_button' ),
  $clear:                  $( '.js-type-and-filter_clear' ),
  $messages:               $( '.js-type-and-filter_message' ),
  allMessage:              'Showing all {{ count }} contacts.',
  filteredMessageSingular: 'There is 1 contact result for "{{ term }}".',
  filteredMessageMultiple: 'There are {{ count }} contact results for "{{ term }}".'
} );

// Hide the contact list header of there are zero results.
$( '.type-and-filter' ).on( 'attemptSearch', function() {
  var resultsCount;
  if ( $( '#contact-list' ).is( ':hidden' ) ) {
    $( '#contact-list' ).show();
    $( '.type-and-filter' ).trigger( 'attemptSearch' );
  } else {
    // Hide the show all contacts button if a search has been performed.
    $( '#contact-list_btn' ).hide();
    // Show the message because on small screens it is hidden until needed.
    $( '.js-type-and-filter_message' ).show();
    // Hide the contact list header of there are zero results.
    resultsCount = $( '.js-type-and-filter_item' ).filter( ':visible' ).length;
    $( '#contact-list_header' ).toggle( resultsCount > 0 );
  }
} );

// Clicking on a helpful term should trigger a filter.
$( '.js-helpful-term' ).on( 'click', function() {
  $( '.js-type-and-filter_input' ).val( $( this ).text() ).trigger( 'valChange' );
  $( '.type-and-filter' ).trigger( 'attemptSearch' );
} );

// Provide a button to expand the contact list
// The contact list is hidden by default on small screens.
$( '#contact-list_btn' ).on( 'click', function() {
  $( this ).hide();
  $( '#contact-list' ).slideDown();
  $( '.js-type-and-filter_message' ).slideDown();
} );
