/* ==========================================================================
   Validators
   Various utility functions to check if a field contains a valid value
   ========================================================================== */


// Required Modules
const ERROR_MESSAGES = require( '../../config/error-messages-config' );
const typeCheckers = require( '../../modules/util/type-checkers' );

/* TODO: Update all the validators to return both passed and failed states
   instead of returning an empty object if the value passed */

/**
 * date Determines if a field contains a valid date.
 *
 * @param {Object} field         Field to test.
 * @param {Object} currentStatus A previous tested status for the field.
 * @returns {Object} An empty object if the field passes,
 *   otherwise an object with msg and type properties if it failed.
 */
function date( field, currentStatus ) {
  const status = currentStatus || {};
  // Date regex matches date patterns allowed in cfgov/v1/forms.py FilterableDateField
  // https://regex101.com/r/JVKCf9/1
  const dateRegex =
    /^\d{4}$|^(?:\d{1}|\d{2})\/(?:\d{4}|\d{2})$|^(?:\d{1}|\d{2})\/(?:\d{1}|\d{2})\/(?:\d{4}|\d{2})$/;
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
 * @param {Object} options       Options object.
 * @returns {Object} An empty object if the field passes,
 *   otherwise an object with msg and type properties if it failed.
 */
function email( field, currentStatus, options ) {
  const status = currentStatus || {};
  const opts = options || {};
  const regex =
    '^[a-z0-9\u007F-\uffff!#$%&\'*+\/=?^_`{|}~-]+(?:\\.[a-z0-9' +
    '\u007F-\uffff!#$%&\'*+\/=?^_`{|}~-]+)*@(?:[a-z0-9]' +
    '(?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z]{2,}$';
  const emailRegex = new RegExp( regex, 'i' );
  const emptyValidation = empty( field );
  const isFilled = typeof emptyValidation.required === 'undefined' ?
    true : emptyValidation.required;
  let state;
  let key;

  if ( !isFilled ) {
    // TODO: Create a language checker instead of doing this inline like this
    state = 'REQUIRED';
    key = opts.language === 'es' ? state + '_ES' : state;

    status.msg = status.msg || '';
    status.msg += ERROR_MESSAGES.EMAIL[key];
    status.email = false;
  } else if ( emailRegex.test( field.value ) === false ) {
    state = 'INVALID';
    key = opts.language === 'es' ? state + '_ES' : state;

    status.msg = status.msg || '';
    status.msg += ERROR_MESSAGES.EMAIL[key];
    status.email = false;
  }
  return status;
}

// TODO: Rename this so it's clearer it's checking a required attribute
/**
 * empty Determines if a required field contains a value.
 *
 * @param {Object} field         Field to test.
 * @param {Object} currentStatus A previous tested status for the field.
 * @returns {Object} An empty object if the field passes,
 *   otherwise an object with msg and type properties if it failed.
 */
function empty( field, currentStatus ) {
  const status = currentStatus || {};
  const isRequired = field.getAttribute( 'required' ) !== null;
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
  const status = currentStatus || {};
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
  const status = currentStatus || {};
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
  let statusMsg = currentStatus.msg || '';
  const required = parseInt( field.getAttribute( 'data-required' ) || 0, 10 );
  const groupFieldsLength = fieldset.length;

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
