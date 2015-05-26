/* ==========================================================================
   Form validation.
   Check to make sure at least one form element has a value before submitting.
   ========================================================================== */

'use strict';

var $ = require( 'jquery' );
require( './jquery/cf_formValidator' ).init();
require( './jquery/cf_notifier' ).init();

function _createMessage( type, label ) {
  var message = {
    required:   'Please fill out the ' + label + ' field.',
    email:      'Please include a valid email address.',
    checkgroup: 'Please select at least one of the ' + label + ' options.'
  };

  return message[type];
}

function _sendError( elem, field ) {
  var label = field.label;
  var type;

  for ( var key in field.status ) {
    if ( field.status.hasOwnProperty( key ) && field.status[key] === false ) {
      type = key;
    }
  }

  $( elem ).trigger( 'cf_notifier:notify', {
    message: _createMessage( type, label ),
    state:   'error'
  } );
  $( field.elem ).addClass( 'error' );
}

function _clearError( elem ) {
  var $elem = $( elem );
  $elem.trigger( 'cf_notifier:clear' );
  $elem.find( '.error' ).removeClass( 'error' );
}

function _sendSubscriptionRequest( elem ) {
  var $form = $( elem );
  var action = $form.attr( 'action' );
  var formData = $form.serialize();
  var states = {
    fail: {
      message: 'There was an error in your submission, please try again later.',
      state:   'error'
    },
    pass: {
      message: 'Your subscription was successfuly received.',
      state:   'success'
    }
  };

  $.post( action, formData, function( data ) {
    $form.trigger( 'cf_notifier:notify', {
      message: states[data.result].message,
      state:   states[data.result].state
    } );
  } );
}

function init() {
  $( 'form' ).cf_formValidator( 'init', {
    onFailure: function( event, fields ) {
      event.preventDefault();
      _sendError( this, fields.invalid[0] );
    },
    onSuccess: function( event ) {
      _clearError( this );
      if ( this.id === 'email-subscribe-form' ) {
        event.preventDefault();
        _sendSubscriptionRequest( this );
      }
    }
  } ).cf_notifier();
}

module.exports = { init: init };
