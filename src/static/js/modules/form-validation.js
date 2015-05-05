/* ==========================================================================
   Form validation.
   Check to make sure at least one form element has a value before submitting.
   ========================================================================== */

'use strict';

var $ = require( 'jquery' );

function init() {
  $( '.js-validate_form-not-empty' ).each( function() {
    var $form = $( this );

    $form.on( 'submit', function() {
      var formIsEmpty = true;
      var event;

      $.each( $form.serializeArray(), function( index, element ) {
        if ( element.value !== '' ) {
          formIsEmpty = false;
        }
      } );

      if ( formIsEmpty ) {
        event = 'form:validate:empty';
      } else {
        event = 'form:validate:not_empty';
      }

      $form.trigger( event, $form );

      return !formIsEmpty;
    } );

    return $form;
  } );
}

module.exports = { init: init };
