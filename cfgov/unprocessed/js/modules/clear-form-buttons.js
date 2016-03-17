/* ==========================================================================
   Clear form button
   - Clear checkboxes and selects
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
    var inputs = $form.find( 'input' );
    $.each(inputs, function() {
      this.remove();
    });

    $form.submit();
  } );
}

// Expose public methods.
module.exports = { init: init };
