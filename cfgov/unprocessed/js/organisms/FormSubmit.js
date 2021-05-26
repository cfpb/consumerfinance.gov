// Required modules.
import { checkDom, setInitFlag } from '@cfpb/cfpb-atomic-component/src/utilities/atomic-helpers.js';
import AlphaTransition from '@cfpb/cfpb-atomic-component/src/utilities/transition/AlphaTransition';
import BaseTransition from '@cfpb/cfpb-atomic-component/src/utilities/transition/BaseTransition';
import ERROR_MESSAGES from '../config/error-messages-config';
import EventObserver from '@cfpb/cfpb-atomic-component/src/mixins/EventObserver.js';
import Notification from '../molecules/Notification';
import { scrollIntoView } from '../modules/util/scroll';

const FORM_MESSAGES = ERROR_MESSAGES.FORM.SUBMISSION;

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
  const _baseElement = checkDom( element, baseClass );
  const _formElement = _baseElement.querySelector( 'form' );
  const _notificationElement = _baseElement.querySelector(
    `.${ Notification.BASE_CLASS }`
  );
  let _notification;
  let _cachedFields;
  const eventObserver = new EventObserver();
  const self = this;
  this.addEventListener = eventObserver.addEventListener;
  this.removeEventListener = eventObserver.removeEventListener;
  this.dispatchEvent = eventObserver.dispatchEvent;

  /**
   * @returns {FormSubmit} An instance.
   */
  function init() {
    if ( !setInitFlag( _baseElement ) ) {
      return this;
    }
    _cachedFields = _cacheFields();
    _formElement.addEventListener( 'submit', _onSubmit );
    _notification = new Notification( _baseElement );
    _notification.init();

    return this;
  }

  /**
   * @param {event} event DOM event
   * @returns {event} DOM event.
   */
  function _onSubmit( event ) {
    event.preventDefault();
    const errors = _validateForm();

    _baseElement.classList.add( 'form-submitted' );

    if ( errors ) {
      _displayNotification( Notification.ERROR, errors );
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
    let UNDEFINED;
    return UNDEFINED;
  }

  /**
   * Displays notification and scrolls it into view if offscreen
   * @param {type} type of notification
   * @param {content} content for notification.
   */
  function _displayNotification( type, content ) {
    _notification.update( type, content );
    _notification.show();
    scrollIntoView( _notificationElement );
  }

  /**
   * Sends form data and displays notification on success / failure.
   * @param {formData} form data object with field name/value pairs
   */
  function _submitForm() {
    const DONE_CODE = 4;
    const SUCCESS_CODES = {
      200: 'ok',
      201: 'created',
      202: 'accepted',
      203: 'non-authoritative info',
      204: 'no content',
      205: 'reset content',
      206: 'partial content'
    };
    let message = '';
    let heading = '';
    let state = 'ERROR';
    const xhr = new XMLHttpRequest();
    xhr.open( 'POST', _formElement.action );
    xhr.setRequestHeader( 'Content-type', 'application/x-www-form-urlencoded' );
    xhr.setRequestHeader( 'X-Requested-With', 'XMLHttpRequest' );
    xhr.onreadystatechange = function() {
      if ( xhr.readyState === DONE_CODE ) {
        if ( xhr.status in SUCCESS_CODES ) {
          let result;
          try {
            const response = JSON.parse( xhr.responseText );
            result = response.result;
            message = response.message || '';
            heading = response.heading || '';
          } catch ( err ) {
            // ignore lack of response
          }
          state = result === 'fail' ? 'ERROR' : 'SUCCESS';
        }
        if ( state === 'SUCCESS' && opts.replaceForm ) {
          _replaceFormWithNotification( heading + ' ' + message );
        } else {
          const key = opts.language === 'es' ? state + '_ES' : state;
          _displayNotification(
            Notification[state],
            message || FORM_MESSAGES[key]
          );
        }
        if ( state === 'SUCCESS' ) {
          self.dispatchEvent( 'success', { target: this, form: _formElement } );
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
    const transition = new AlphaTransition( _baseElement ).init();
    scrollIntoView( _formElement, { offset: 100, callback: fadeOutForm } );

    function fadeOutForm() {
      transition.addEventListener( BaseTransition.END_EVENT, fadeInMessage );
      transition.fadeOut();
    }

    function fadeInMessage() {
      _notification.update( Notification.SUCCESS, message );
      _notification.show();
      _baseElement.replaceChild( _notificationElement, _formElement );
      transition.removeEventListener( BaseTransition.END_EVENT, fadeInMessage );
      transition.fadeIn();
    }
  }

  /**
   * @returns {obj} form fields, keyed by name.
   *   Checkboxes and radio fields are stored in array.
   */
  function _cacheFields() {
    const nonInputTypes = [ 'file', 'reset', 'submit', 'button' ];
    const cachedFields = {};
    const fields = ( _formElement || {} ).elements;
    for ( let f = 0; f < fields.length; f++ ) {
      const field = fields[f];
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
    const data = [];
    Object.keys( _cachedFields ).forEach( function( fieldName ) {
      const field = _cachedFields[fieldName];
      if ( field.type === 'select-multiple' && field.options ) {
        const options = field.options;
        for ( let i = 0; i < options.length; i++ ) {
          const option = options[i];
          if ( option.selected ) {
            data.push( _serializeField( fieldName, option.value ) );
          }
        }
      } else if ( Array.isArray( field ) ) {
        for ( let f = 0; f < field.length; f++ ) {
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

export default FormSubmit;
