'use strict';

// Required modules.
var atomicHelpers = require( '../modules/util/atomic-helpers' );
var ERROR_MESSAGES = require( '../config/error-messages-config' );
var getClosestElement = require( '../modules/util/dom-traverse' ).closest;
var Notification = require( '../molecules/Notification' );
var typeCheckers = require( '../modules/util/type-checkers' );

/**
 * FilterableListControls
 * @class
 *
 * @classdesc Initializes a new Filterable-List-Controls organism.
 *
 * @param {HTMLNode} element
 *   The DOM element within which to search for the organism.
 */
function FilterableListControls( element ) {
  var BASE_CLASS = 'o-filterable-list-controls';
  var _dom = atomicHelpers.checkDom(
    element, BASE_CLASS, 'FilterableListControls' );
  var _form = _dom.querySelector( 'form' );
  var _notification;
  var _fieldGroups;

  var _defaults = {
    ignoreFieldTypes: [
      'hidden',
      'button',
      'submit',
      'reset',
      'fieldset'
    ],
    groupFieldTypes: [
      'radio',
      'checkbox'
    ]
  };

  var _validators = {
    date: function( field, currentStatus ) {
      var status = currentStatus || {};
      var dateRegex =
        /^\d{2}$|^\d{4}$|^\d{2}\/(?:\d{4}|\d{2})$|^\d{2}\/\d{2}\/\d{4}$/;
      if ( field.value && dateRegex.test( field.value ) === false ) {
        status.msg += ERROR_MESSAGES.DATE.INVALID;
        status.date = false;
      }
      return status;
    },
    email: function( field, currentStatus ) {
      var status = currentStatus || {};
      var regex = [ "^[a-z0-9\u007F-\uffff!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9",
                    "\u007F-\uffff!#$%&'*+\/=?^_`{|}~-]+)*@(?:[a-z0-9]",
                    "(?:[a-z0-9-]*[a-z0-9])?\.)+[a-z]{2,}$" ].join( '' );
      var emailRegex = new RegExp( regex, 'i' );
      if ( field.value && emailRegex.test( field.value ) === false ) {
        status.msg += ERROR_MESSAGES.EMAIL.INVALID;
        status.email = false;
      }
      return status;
    },
    empty: function( field, currentStatus ) {
      var status = currentStatus || {};
      var isRequired = field.getAttribute( 'required' ) !== null;
      if ( isRequired && typeCheckers.isEmpty( field.value ) ) {
        status.msg += ERROR_MESSAGES.FIELD.REQUIRED;
        status.required = false;
      }
      return status;
    },
    checkbox: function( field, currentStatus, type ) {
      var status = currentStatus || {};
      var groupName = field.getAttribute( 'data-group' ) ||
                      field.getAttribute( 'name' );
      var groupSelector = '[name=' + groupName + ']:checked,' +
                          '[data-group=' + groupName + ']:checked';
      var groupFields = _form.querySelectorAll( groupSelector );
      var groupFieldsLength = ( groupFields || [] ).length;
      var required = parseInt( field.getAttribute( 'data-required' ) ||
                               0, 10 );
      if ( groupFieldsLength < required ) {
        status[type || 'checkbox'] = false;
        status.msg = ERROR_MESSAGES.CHECKBOX.REQUIRED.replace( '%s', required );
      }
      return status;
    },
    radio: function( field, currentStatus ) {
      return _validators.checkbox( field, currentStatus, 'radio' );
    }
  };

  /**
   * Initialize FilterableListControls instance.
   */
  function init( ) {
    _notification = new Notification( _dom );
    _notification.init();

    _initEvents();
  }

  /**
   * Initialize FilterableListControls events.
   */
  function _initEvents() {
    _form.addEventListener( 'submit', _formSubmitted );
  }

  /**
   * Remove Event listeners.
   */
  function destroy() {
    _form.removeEventListener( 'submit', _formSubmitted );
  }

  /**
   * Show error notification.
   * @param {Object} event Form submitted event.
   */
  function _formSubmitted( event ) {
    var validatedFields = _validateFields( [].slice.call( _form.elements ) );

    if ( validatedFields.invalid.length > 0 ) {
      event.preventDefault();
      _setNotification( _notification.ERROR,
                        _buildErrorMessage( validatedFields.invalid ) );
    }
  }

  /**
   * Build the error message to display within the notification.
   * @param {Array} fields A list of form fields.
   * @returns {string} A text to use for the error notification.
   */
  function _buildErrorMessage( fields ) {
    var msg = '';
    fields.forEach( function( validation ) {
      msg += validation.label + ' ' + validation.msg + '</br>';
    } );

    return msg || ERROR_MESSAGES.DEFAULT;
  }

  /**
   * Validate the fields of our form.
   * @param {HTMLNode} field A form field.
   * @param {string} selector Selector used to retreive the dom element.
   * @param {boolean} isInGroup Flag used determine if field is in group.
   * @returns {string} The label of the field.
   */
  function _getLabelText( field, selector, isInGroup ) {
    var labelText = '';
    var labelDom;

    if ( isInGroup && !selector ) {
      labelDom = getClosestElement( field, 'fieldset' );
      if ( labelDom ) labelDom = labelDom.querySelector( 'legend' );
    } else {
      selector = selector ||
                 'label[for="' + field.getAttribute( 'id' ) + '"]';
      labelDom = _form.querySelector( selector );
    }

    if ( labelDom ) labelText = labelDom.textContent.trim();

    return labelText;
  }

  /**
   * Set the notification type, msg, and visibility.
   * @param {string} type The type of notification to display.
   * @param {string} msg The message to display in the notification.
   * @param {string} methodName The method to use to control visibility
                                of the notification.
   */
  function _setNotification( type, msg, methodName ) {
    methodName = methodName || 'show';
    _notification.setTypeAndContent( type, msg );
    _notification[methodName]();
  }

  /**
   * Determines if you should validate a field.
   * @param {HTMLNode} field A form field.
   * @param {string} type The type of field.
   * @param {boolean} isInGroup A boolean that determines if field in a group.
   * @returns {boolean} Value indicating whether to validate a field.
   */
  function shouldValidateField( field, type, isInGroup ) {
    var isDisabled = field.getAttribute( 'disabled' ) !== null;
    var isIgnoreType = _defaults.ignoreFieldTypes.indexOf( type ) > -1;
    var shouldValidate = isDisabled === false && isIgnoreType === false;

    if ( shouldValidate && isInGroup ) {
      var name = field.getAttribute( 'data-group' ) ||
                 field.getAttribute( 'name' );
      var isRequired = field.getAttribute( 'data-required' ) !== null;
      var groupExists = _fieldGroups.indexOf( name ) > -1;
      if ( groupExists || isRequired === false ) {
        shouldValidate = false;
      } else {
        _fieldGroups.push( name );
      }
    }

    return shouldValidate;
  }

  /**
   * Validate the fields of our form.
   * @param {Array} fields A list of form fields.
   * @returns {Object}
   *   The tested list of fields broken into valid and invalid blocks.
   */
  function _validateFields( fields ) {
    var validatedFields = {
      invalid: [],
      valid:   []
    };
    var validatedField;

    _fieldGroups = [];

    fields.forEach( function loopFields( field ) {
      var fieldIsValid = true;
      var type = field.getAttribute( 'data-type' ) ||
                 field.getAttribute( 'type' ) ||
                 field.tagName.toLowerCase();
      var isGroupField = _defaults.groupFieldTypes.indexOf( type ) > -1;

      if ( shouldValidateField( field, type, isGroupField ) === false ) return;

      validatedField = _validateField( field, type, isGroupField );

      for ( var prop in validatedField.status ) {
        if ( validatedField.status[prop] === false ) fieldIsValid = false;
      }

      if ( fieldIsValid ) {
        validatedFields.valid.push( validatedField );
      } else {
        validatedFields.invalid.push( validatedField );
      }
    } );

    return validatedFields;
  }

  /**
   * Validate the specific field types.
   * @param {HTMLNode} field A form field.
   * @param {string} type The type of field.
   * @param {boolean} isInGroup A boolean that determines if field in a group.
   * @returns {Object} An object with a status and message properties.
   */
  function _validateField( field, type, isInGroup ) {
    var validation = {
      field:      field,
      // TODO: Change layout of field groups to use fieldset.
      label:      _getLabelText( field, '', false || isInGroup ),
      msg:        '',
      status:     null
    };

    if ( _validators[type] ) {
      validation.status = _validators[type]( field, validation );
    }

    return _validators.empty( field, validation );
  }

  this.init = init;
  this.destroy = destroy;
  return this;
}

module.exports = FilterableListControls;
