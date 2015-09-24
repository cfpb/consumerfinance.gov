/* ==========================================================================
   Clear form button
   - Clear checkboxes and selects
   - Clear Chosen.js elements
   - Clear jquery.custom-input elements
   ========================================================================== */

'use strict';

var $ = require( 'jquery' );

/**
 * Set up DOM references, attributes, and event handlers.
 */
function init() {
  $( '.js-form_clear' ).on( 'click', function() {
    var $this = $( this );
    var $form = $this.parents( 'form' );

    // Clear text inputs
    $form.find( 'input[type="text"]' ).val( '' );

    // Clear checkboxes
    $form.find( '[type="checkbox"]' )
    .removeAttr( 'checked' );

    // Clear select options
    $form.find( 'select option' )
    .removeAttr( 'selected' );
    $form.find( 'select option:first' )
    .attr( 'selected', true );

    // Clear .custom-input elements
    $form.find( '.custom-input' )
    .trigger( 'updateState' );

    // Clear .custom-select elements
    $form.find( '.custom-select_select' )
    .trigger( 'updateState' );

    // Clear Chosen.js elements
    $form.find( '.chosen-select' )
    .val( '' )
    .trigger( 'chosen:updated' );
  } );
}

// Expose public methods.
module.exports = { init: init };
