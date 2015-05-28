/* ==========================================================================
 * Show/Hide Additional Fields
 *
 * Shows additional fields on forms when additional information is needed
 *
 * ========================================================================== */

'use strict';

var $ = require( 'jquery' );

function init() {

  function toggleAdditionalFields( input ) {
    var additionalFields = $( input ).attr('data-additional-fields');

    if ( $( input ).is(':checked') ) {
      $( additionalFields ).show();
    } else {
      $( additionalFields ).hide();
    }
  }

  // Show or hide additional fields when any radio button in fieldset changes
  $( '.js-additional-field' ).on('change', function() {
    var showField = $( this ).find( '.js-additional-field_trigger');
    toggleAdditionalFields( showField );
  } );


  // Show or hide additional fields on init
  $( '.js-additional-field' ).each( function ( i ) {
    var showField = $( this ).find( '.js-additional-field_trigger');
    toggleAdditionalFields( showField );
  } );
}

module.exports = { init: init };
