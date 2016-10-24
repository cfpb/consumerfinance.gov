'use strict';

// Required modules.
var atomicHelpers = require( '../modules/util/atomic-helpers' );
var ERROR_MESSAGES = require( '../config/error-messages-config' );
var FORM_MESSAGES = ERROR_MESSAGES.FORM.SUBMISSION;
var Notification = require( '../molecules/Notification' );

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
  var BASE_CLASS = 'o-email-signup';
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
   * @param {HTMLNode} event
   * @returns {event} DOM event.
   */
  function _onSubmit( event ) {
    event.preventDefault();
    if ( !_emailElement.value ) {
      return UNDEFINED;
    }
    if ( isValidEmail( _emailElement ) === false ) {
      _notification.setTypeAndContent( _notification.ERROR,
                                       ERROR_MESSAGES.EMAIL.INVALID );
      _notification.show();
    } else {
      sendEmail();
    }

    return event;
  }

  /**
   * Sends form data and displays notification on success / failure.
   */
  function sendEmail( ) {
    var DONE_CODE = 4;
    var SUCCESS_CODES = [ 200, 201, 202, 203, 204, 205, 206 ];
    var notificationType = _notification.ERROR;
    var notificationMsg = FORM_MESSAGES.ERROR;
    var xhr = new XMLHttpRequest();
    xhr.open( 'POST', _formElement.action );
    xhr.setRequestHeader( 'Content-type', 'application/x-www-form-urlencoded' );
    xhr.setRequestHeader( 'X-Requested-With', 'XMLHttpRequest' );
    xhr.onreadystatechange = function() {
      if ( xhr.readyState === DONE_CODE ) {
        // TODO: It might make sense to use min / max instead.
        if ( SUCCESS_CODES.indexOf( xhr.status ) > -1 ) {
          notificationType = _notification.SUCCESS;
          notificationMsg = FORM_MESSAGES.SUCCESS;
        }
        _notification.setTypeAndContent( notificationType, notificationMsg );
        _notification.show();
      }
    };
    xhr.send( serializeFormData() );
  }

  /**
   * Determines if a field contains a valid email.
   *
   * @param {HTMLNode} element Form field.
   * @returns {Boolean} indicating if the field is valid email.
   */
  function isValidEmail( element ) {
    var regex =
      '^[a-z0-9\u007F-\uffff!#$%&\'*+\\/=?^_`{|}~-]+(?:\\.[a-z0-9' +
      '\u007F-\uffff!#$%&\'*+\\/=?^_`{|}~-]+)*@(?:[a-z0-9]' +
      '(?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z]{2,}$';
    var emailRegex = new RegExp( regex, 'i' );
    var isValid = true;
    if ( emailRegex.test( element.value ) === false ) {
      isValid = false;
    }
    return isValid;
  }

  /**
   * @returns {string} representing form data.
   */
  function serializeFormData() {
    return [ _emailElement, _codeElement ].map( function( formElement ) {
      return encodeURIComponent( formElement.name ) +
      '=' + encodeURIComponent( formElement.value );
    } ).join( '&' );
  }

  this.init = init;

  return this;
}

EmailSignup.selector = '.o-email-signup';

module.exports = EmailSignup;
