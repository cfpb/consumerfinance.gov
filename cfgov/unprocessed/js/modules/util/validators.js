/* ==========================================================================
   Validators

   Various utility functions to check if a field contains a valid value
   ========================================================================== */

'use strict';

// Required Modules
var ERROR_MESSAGES = require( '../../config/error-messages-config' );
var typeCheckers = require( '../../modules/util/type-checkers' );

/**
 * date Determines if a field contains a valid date.
 *
 * @param {Object} field         Field to test.
 * @param {Object} currentStatus A previous tested status for the field.
 * @returns {Object} An empty object if the field passes,
 *   otherwise an object with msg and type properties if it failed.
 */
function date( field, currentStatus ) {
  var status = currentStatus || {};
  var dateRegex =
    /^\d{2}$|^\d{4}$|^\d{2}\/(?:\d{4}|\d{2})$|^\d{2}\/\d{2}\/\d{4}$/;
  if ( field.value && dateRegex.test( field.value ) === false ) {
    status.msg = status.msg || '';
    status.msg += ERROR_MESSAGES.DATE.INVALID;
    status.date = false;
  }
  return status;
}

/**
 * email Determines if a field contains a email date.
 *
 * @param {Object} field         Field to test.
 * @param {Object} currentStatus A previous tested status for the field.
 * @returns {Object} An empty object if the field passes,
 *   otherwise an object with msg and type properties if it failed.
 */
function email( field, currentStatus ) {
  var status = currentStatus || {};
  var regex =
    '^[a-z0-9\u007F-\uffff!#$%&\'*+\/=?^_`{|}~-]+(?:\\.[a-z0-9' +
    '\u007F-\uffff!#$%&\'*+\/=?^_`{|}~-]+)*@(?:[a-z0-9]' +
    '(?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z]{2,}$';
  var emailRegex = new RegExp( regex, 'i' );
  if ( field.value && emailRegex.test( field.value ) === false ) {
    status.msg = status.msg || '';
    status.msg += ERROR_MESSAGES.EMAIL.INVALID;
    status.email = false;
  }
  return status;
}

/**
 * empty Determines if a required field contains a value.
 *
 * @param {Object} field         Field to test.
 * @param {Object} currentStatus A previous tested status for the field.
 * @returns {Object} An empty object if the field passes,
 *   otherwise an object with msg and type properties if it failed.
 */
function empty( field, currentStatus ) {
  var status = currentStatus || {};
  var isRequired = field.getAttribute( 'required' ) !== null;
  if ( isRequired && typeCheckers.isEmpty( field.value ) ) {
    status.msg = status.msg || '';
    status.msg += ERROR_MESSAGES.FIELD.REQUIRED;
    status.required = false;
  }
  return status;
}

/**
 * checkbox
 * Determines if a field contains a required number of picked checkbox options.
 *
 * @param {Object} field         Field to test.
 * @param {Object} currentStatus A previous tested status for the field.
 * @param {Array}  fieldset      A list of fields related to the parent field.
 * @returns {Object} An empty object if the field passes,
 *   otherwise an object with msg and type properties if it failed.
 */
function checkbox( field, currentStatus, fieldset ) {
  var status = currentStatus || {};
  return _checkableInput( field, status, fieldset, 'checkbox' );
}

/**
 * radio Determines if a field contains a picked radio option.
 *
 * @param {Object} field         Field to test.
 * @param {Object} currentStatus A previous tested status for the field.
 * @param {Array}  fieldset      A list of fields related to the parent field.
 * @returns {Object} An empty object if the field passes,
 *   otherwise an object with msg and type properties if it failed.
 */
function radio( field, currentStatus, fieldset ) {
  var status = currentStatus || {};
  return _checkableInput( field, status, fieldset, 'radio' );
}

/**
 * _checkableInput
 * Determines if a field contains a required number of
 * picked checkbox or radio button options.
 *
 * @param {Object} field         Field to test.
 * @param {Object} currentStatus A previous tested status for the field.
 * @param {Array}  fieldset      A list of fields related to the parent field.
 * @param {string} type          Should be "radio" or "checkbox".
 * @returns {Object} An empty object if the field passes,
 *   otherwise an object with msg and type properties if it failed.
 */
function _checkableInput( field, currentStatus, fieldset, type ) {
  var statusMsg = currentStatus.msg || '';
  var required = parseInt( field.getAttribute( 'data-required' ) || 0, 10 );
  var groupFieldsLength = fieldset.length;

  if ( groupFieldsLength < required ) {
    statusMsg += ERROR_MESSAGES.CHECKBOX.REQUIRED.replace( '%s', required );
    currentStatus.msg = statusMsg;
    currentStatus[type] = false;
  }

  return currentStatus;
}

module.exports = {
  date:     date,
  email:    email,
  empty:    empty,
  checkbox: checkbox,
  radio:    radio
};
