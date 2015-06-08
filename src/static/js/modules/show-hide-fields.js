/* ==========================================================================
 * Show/Hide Additional Fields
 * This is for form pages on Office templates.
 * Shows additional fields on forms when additional information is needed.
 *
 * Set the id for fieldset with additional fields with the data-attribute
 * `data-additional-fields`
 *
 * Set the fieldset to monitor for changes with class
 * `.js-additional-field_trigger`
 *
 * Set the input which triggers the change with `.js-additional-field_trigger`
 *
 * ========================================================================== */

'use strict';

var $ = require( 'jquery' );

function _toggleAdditionalFields( input ) {
  var additionalFields = $( input ).attr( 'data-additional-fields' );

  if ( $( input ).is( ':checked' ) ) {
    $( additionalFields ).find( 'input, select, textarea' ).each( function() {
      $( this ).prop( 'disabled', false );
    } );
    $( additionalFields ).removeClass( 'js-is-hidden' );

  } else {
    $( additionalFields ).find( 'input, select, textarea' ).each( function() {
      $( this ).prop( 'disabled', true );
    } );
    $( additionalFields ).addClass( 'js-is-hidden' );
  }
}

function init() {
  // Show or hide additional fields when any radio button in fieldset changes
  $( '.js-additional-field' ).on( 'change', function() {
    var showField = $( this ).find( '.js-additional-field_trigger' );
    _toggleAdditionalFields( showField );
  } );
}

module.exports = { init: init };
