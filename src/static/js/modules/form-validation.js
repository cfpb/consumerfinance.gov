/* ==========================================================================
   Form validation.
   Check to make sure at least one form element has a value before submitting.
   ========================================================================== */

'use strict';

var $ = require( 'jquery' );
require( './jquery/cf_formValidator' ).init();
require( './jquery/cf_notifier' ).init();

function _sendNotification( elem, field ) {
  var label = field.label;
  var type;
  var message;

  for ( var key in field.status ) {
    if ( field.status.hasOwnProperty(key) && field.status[key] === false ) {
      type = key;
    }
  }

  if ( type === 'required' ) {
    message = 'Please fill out the ' + label + ' field.';
  }

  if ( type === 'email' ) {
    message = 'Please include a valid email address.';
  }

  if ( type === 'checkgroup' ) {
    message = 'Please select at least one of the ' + label + ' options.';
  }

  $( elem ).trigger( 'cf_notifier:notify', {
    message: message
  } );
  $( field.elem ).addClass( 'error' );
}

function _clearNotification( elem ) {
  var $elem = $( elem );
  $elem.trigger( 'cf_notifier:clear' );
  $elem.find('.error').removeClass( 'error' );
}

function init() {
  $( 'form' ).cf_formValidator( 'init', {
    onFailure: function( event, fields ) {
      event.preventDefault();
      _sendNotification( this, fields.invalid[0] );
    },
    onSuccess: function( event, fields ) {
      _clearNotification( this );
    }
  } ).cf_notifier();
}

module.exports = { init: init };
