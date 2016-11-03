'use strict';

// Required modules.
var atomicHelpers = require( '../modules/util/atomic-helpers' );
var ERROR_MESSAGES = require( '../config/error-messages-config' );
var FORM_MESSAGES = ERROR_MESSAGES.FORM.SUBMISSION;
var Notification = require( '../molecules/Notification' );
var validateEmail = require( '../modules/util/validators' ).email;
var BASE_CLASS = 'o-email-signup';

/**
 * EmailSignup
 * @class
 *
 * @classdesc Initializes the organism.
 *
 * @param {HTMLNode} element
 *   The DOM element within which to search for the organism.
 * @returns {EmailSignup} An instance.
 */
function EmailSignup( element ) {
  var UNDEFINED;
  var _baseElement = atomicHelpers.checkDom( element, BASE_CLASS );
  var _formElement = _baseElement.querySelector( 'form' );
  var _emailElement = _formElement.querySelector( 'input[type="email"]' );
  var _codeElement = _formElement.querySelector( 'input[name="code"]' );
  var _notification = new Notification( _baseElement );

  /**
   * @returns {EmailSignup|undefined} An instance,
   *   or undefined if it was already initialized.
   */
  function init() {
    if ( !atomicHelpers.setInitFlag( _baseElement ) ) {
      return UNDEFINED;
    }

    _formElement.addEventListener( 'submit', _onSubmit );

    return this;
  }

  /**
   * @param {event} event DOM event
   * @returns {event} DOM event.
   */
  function _onSubmit( event ) {
    var isValid;
    event.preventDefault();
    if ( !_emailElement.value ) {
      return UNDEFINED;
    }
    isValid = validateEmail( _emailElement );
    if ( isValid.email === false ) {
      _notification.setTypeAndContent( _notification.ERROR,
                                       ERROR_MESSAGES.EMAIL.INVALID );
      _notification.show();
    } else {
      _sendEmail();
    }

    return event;
  }

  /**
   * Sends form data and displays notification on success / failure.
   */
  function _sendEmail( ) {
    var DONE_CODE = 4;
    var SUCCESS_CODES = {
      200: 'ok',
      201: 'created',
      202: 'accepted',
      203: 'non-authoritative info',
      204: 'no content',
      205: 'reset content',
      206: 'partial content'
    };
    var notificationType = _notification.ERROR;
    var notificationMsg = FORM_MESSAGES.ERROR;
    var xhr = new XMLHttpRequest();
    xhr.open( 'POST', _formElement.action );
    xhr.setRequestHeader( 'Content-type', 'application/x-www-form-urlencoded' );
    xhr.setRequestHeader( 'X-Requested-With', 'XMLHttpRequest' );
    xhr.onreadystatechange = function() {
      if ( xhr.readyState === DONE_CODE ) {
        if ( xhr.status in SUCCESS_CODES ) {
          notificationType = _notification.SUCCESS;
          notificationMsg = FORM_MESSAGES.SUCCESS;
        }
        _notification.setTypeAndContent( notificationType, notificationMsg );
        _notification.show();
      }
    };
    xhr.send( _serializeFormData() );
  }

  /**
   * @returns {string} representing form data.
   * Example: param1=value1&param2=value2
   */
  function _serializeFormData() {
    return [ _emailElement, _codeElement ].map( function( formElement ) {
      return encodeURIComponent( formElement.name ) +
      '=' + encodeURIComponent( formElement.value );
    } ).join( '&' );
  }

  this.init = init;

  return this;
}

EmailSignup.BASE_CLASS = '.' + BASE_CLASS;

module.exports = EmailSignup;
