'use strict';
// Required modules.
var atomicHelpers = require( '../modules/util/atomic-helpers' );
var scroll = require( '../modules/util/scroll' );
var AlphaTransition = require( '../modules/transition/AlphaTransition' );
var BaseTransition = require( '../modules/transition/BaseTransition' );
var ERROR_MESSAGES = require( '../config/error-messages-config' );
var FORM_MESSAGES = ERROR_MESSAGES.FORM.SUBMISSION;
var Notification = require( '../molecules/Notification' );
var EventObserver = require( '../modules/util/EventObserver' );

/**
 * FormSubmit
 * @class
 *
 * @classdesc Initializes the organism.
 *
 * @param {HTMLNode} element
 *   The DOM element within which to search for the organism.
 * @param {string} baseClass class of organism
 * @param {Object} opts optional params, including
 *   validator: validation function, and
 *   replaceForm: Boolean, determines if form is replaced with message
 * @returns {FormSubmit} An instance.
 */
function FormSubmit( element, baseClass, opts ) {
  opts = opts || {};
  var UNDEFINED;
  var _baseElement = atomicHelpers.checkDom( element, baseClass );
  var _formElement = _baseElement.querySelector( 'form' );
  var _notificationElement = _baseElement.querySelector( '.m-notification' );
  var _notification = new Notification( _baseElement );
  var _cachedFields;
  var eventObserver = new EventObserver();
  var self = this;
  this.addEventListener = eventObserver.addEventListener;
  this.removeEventListener = eventObserver.removeEventListener;
  this.dispatchEvent = eventObserver.dispatchEvent;

  /**
   * @returns {FormSubmit|undefined} An instance,
   *   or undefined if it was already initialized.
   */
  function init() {
    if ( !atomicHelpers.setInitFlag( _baseElement ) ) {
      return UNDEFINED;
    }
    _cachedFields = _cacheFields();
    _formElement.addEventListener( 'submit', _onSubmit );

    return this;
  }

  /**
   * @param {event} event DOM event
   * @returns {event} DOM event.
   */
  function _onSubmit( event ) {
    event.preventDefault();
    var errors = _validateForm();

    _baseElement.classList.add( 'form-submitted' );

    if ( errors ) {
      _displayNotification( _notification.ERROR, errors );
    } else {
      _submitForm();
    }

    return event;
  }

  /**
   * @returns {string|undefined} error message.
   */
  function _validateForm() {
    if ( typeof opts.validator === 'function' ) {
      return opts.validator( _cachedFields );
    }
    return UNDEFINED;
  }

  /**
   * Displays notification and scrolls it into view if offscreen
   * @param {type} type of notification
   * @param {content} content for notification.
   */
  function _displayNotification( type, content ) {
    _notification.setTypeAndContent( type, content );
    _notification.show();
    scroll.scrollIntoView( _notificationElement );
  }

  /**
   * Sends form data and displays notification on success / failure.
   * @param {formData} form data object with field name/value pairs
   */
  function _submitForm() {
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
    var message = '';
    var heading = '';
    var state = 'ERROR';
    var xhr = new XMLHttpRequest();
    xhr.open( 'POST', _formElement.action );
    xhr.setRequestHeader( 'Content-type', 'application/x-www-form-urlencoded' );
    xhr.setRequestHeader( 'X-Requested-With', 'XMLHttpRequest' );
    xhr.onreadystatechange = function() {
      if ( xhr.readyState === DONE_CODE ) {
        if ( xhr.status in SUCCESS_CODES ) {
          var result;
          try {
            var response = JSON.parse( xhr.responseText );
            result = response.result;
            message = response.message || '';
            heading = response.header || '';
          } catch ( err ) {
            // ignore lack of response
          }
          state = result === 'fail' ? 'ERROR' : 'SUCCESS';
        }
        console.log(message)
        console.log(heading)
        if ( state === 'SUCCESS' && opts.replaceForm ) {
          //heading = heading || 'Thank you!';
          _replaceFormWithNotification( heading + ' ' + message );
        } else {
          var key = opts.language === 'es' ? state + '_ES' : state;
          console.log(key)
          console.log(FORM_MESSAGES[key])
 
           _displayNotification( _notification[state],
                                 message || FORM_MESSAGES[key] );
        }
        if ( state === 'SUCCESS' ) {
          self.dispatchEvent( 'success', { target: this, form: _formElement} );
        }
      }
    };
    xhr.send( _serializeFormData() );
  }

  /**
   * @param {string} message Success message to display
   *  Replaces form with notification on success.
   */
  function _replaceFormWithNotification( message ) {
    var transition = new AlphaTransition( _baseElement ).init();
    scroll.scrollIntoView( _formElement, { offset: 100, callback: fadeOutForm } );

    function fadeOutForm() {
      transition.addEventListener( BaseTransition.END_EVENT, fadeInMessage );
      transition.fadeOut();
    }

    function fadeInMessage() {
      if ( opts.minReplacementHeight ) {
        _baseElement.style.marginBottom = Math.min( _formElement.offsetHeight, 100 ) + 'px';
      }
      _formElement.style.display = 'none';
      _notification.setTypeAndContent( _notification.SUCCESS, message );
      _notification.show();
      transition.removeEventListener( BaseTransition.END_EVENT, fadeInMessage );
      transition.fadeIn();
    }
  }

  /**
   * @returns {obj} form fields, keyed by name.
   *   Checkboxes and radio fields are stored in array.
   */
  function _cacheFields() {
    var nonInputTypes = [ 'file', 'reset', 'submit', 'button' ];
    var cachedFields = {};
    var fields = ( _formElement || {} ).elements;
    for ( var f = 0; f < fields.length; f++ ) {
      var field = fields[f];
      if ( field.name && !field.disabled && nonInputTypes.indexOf( field.type ) === -1 ) {
        if ( field.type === 'radio' || field.type === 'checkbox' ) {
          cachedFields[field.name] = cachedFields[field.name] || [];
          cachedFields[field.name].push( field );
        } else {
          cachedFields[field.name] = field;
        }
      }
    }
    return cachedFields;
  }

  /**
   * @param {string} fieldName name of field
   * @param {string} fieldValue value of field
   * @returns {string} representing field data.
   * Example: param1=value1
   */
  function _serializeField( fieldName, fieldValue ) {
    return encodeURIComponent( fieldName ) + '=' +
           encodeURIComponent( fieldValue );
  }

  /**
   * @returns {string} representing form data.
   * Example: param1=value1&param2=value2
   */
  function _serializeFormData() {
    var data = [];
    Object.keys( _cachedFields ).forEach( function( fieldName ) {
      var field = _cachedFields[fieldName];
      if ( field.type === 'select-multiple' && field.options ) {
        var options = field.options;
        for ( var i = 0; i < options.length; i++ ) {
          var option = options[i];
          if ( option.selected ) {
            data.push( _serializeField( fieldName, option.value ) );
          }
        }
      } else if ( Array.isArray( field ) ) {
        for ( var f = 0; f < field.length; f++ ) {
          if ( field[f].checked ) {
            data.push( _serializeField( fieldName, field[f].value ) );
          }
        }
      } else {
        data.push( _serializeField( fieldName, field.value ) );
      }
    } );

    return data.join( '&' ).replace( /%20/g, '+' );
  }

  this.init = init;

  return this;
}

module.exports = FormSubmit;
