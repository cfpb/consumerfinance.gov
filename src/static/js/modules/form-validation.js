/* ==========================================================================
   Form validation.
   Check to make sure at least one form element has a value before submitting.
   ========================================================================== */

'use strict';

var $ = require( 'jquery' );
require( './jquery/cf_formValidator' ).init();
require( './jquery/cf_notifier' ).init();

function _createMessage( type, label ) {
  var message;

  switch ( type ) {
    case 'required':
      message = 'Please fill out the ' + label + ' field.';
      break;
    case 'email':
      message = 'Please include a valid email address.';
      break;
    case 'checkgroup':
      message = 'Please select at least one of the ' + label + ' options.';
      break;
    default:
      break;
  }
  return message;
}

function _sendNotification( elem, field ) {
  var label = field.label;
  var type;

  for ( var key in field.status ) {
    if ( field.status.hasOwnProperty( key ) && field.status[key] === false ) {
      type = key;
    }
  }

  $( elem ).trigger( 'cf_notifier:notify', {
    message: _createMessage( type, label )
  } );
  $( field.elem ).addClass( 'error' );
}

function _clearNotification( elem ) {
  var $elem = $( elem );
  $elem.trigger( 'cf_notifier:clear' );
  $elem.find( '.error' ).removeClass( 'error' );
}

function _sendSubscriptionRequest( elem ) {
  var $form = $( elem );
  var action = $form.attr( 'action' );
  var formData = $form.serialize();

  $.post( action, formData, function( data ) {
    if ( data.result === 'fail' ) {
      $form.trigger( 'cf_notifier:notify', {
        message: 'There was an error in your submission, please try again later.',
        state:   'error'
      } );
    } else {
      $form.trigger( 'cf_notifier:notify', {
        message: 'Your subscription was successfuly received.',
        state:   'success'
      } );
    }
  } );
}

function init() {
  $( 'form' ).cf_formValidator( 'init', {
    onFailure: function( event, fields ) {
      event.preventDefault();
      _sendNotification( this, fields.invalid[0] );
    },
    onSuccess: function( event ) {
      _clearNotification( this );
      if ( this.id === 'email-subscribe-form' ) {
        event.preventDefault();
        _sendSubscriptionRequest( this );
      }
    }
  } ).cf_notifier();
}

module.exports = { init: init };
