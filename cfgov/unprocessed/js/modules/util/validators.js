/* ==========================================================================
   Validators
   Various utility functions to check if a field contains a valid value
   ========================================================================== */

// Required Modules
import { isEmpty } from '@cfpb/cfpb-design-system';

const ERROR_MESSAGES = {
  EMAIL: {
    INVALID: 'You have entered an invalid email address.',
    INVALID_ES: 'La dirección de correo electrónico introducida no es válida.',
    REQUIRED: 'Please enter an email address.',
    REQUIRED_ES: 'Por favor, introduzca una dirección de correo electrónico.',
  },
};

/**
 * email Determines if a field contains an email address.
 * @param {object} field - Field to test.
 * @param {object} currentStatus - A previous tested status for the field.
 * @param {object} options - Options object.
 * @returns {object} An empty object if the field passes,
 *   otherwise an object with msg and type properties if it failed.
 */
function email(field, currentStatus, options) {
  const status = currentStatus || {};
  const opts = options || {};
  const regex =
    "^[a-z0-9\u007F-\uffff!#$%&'*+/=?^_`{|}~-]+(?:\\.[a-z0-9" +
    "\u007F-\uffff!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9]" +
    '(?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z]{2,}$';
  const emailRegex = new RegExp(regex, 'i');
  const emptyValidation = _empty(field);
  const isFilled =
    typeof emptyValidation.required === 'undefined'
      ? true
      : emptyValidation.required;
  let state;
  let key;

  if (!isFilled) {
    // TODO: Create a language checker instead of doing this inline like this
    state = 'REQUIRED';
    key = opts.language === 'es' ? state + '_ES' : state;

    status.msg = status.msg || '';
    status.msg += ERROR_MESSAGES.EMAIL[key];
    status.email = false;
  } else if (emailRegex.test(field.value) === false) {
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
 * @param {object} field - Field to test.
 * @param {object} currentStatus - A previous tested status for the field.
 * @returns {object} An empty object if the field passes,
 *   otherwise an object with msg and type properties if it failed.
 */
function _empty(field, currentStatus) {
  const status = currentStatus || {};
  const isRequired = field.getAttribute('required') !== null;
  if (isRequired && isEmpty(field.value)) {
    status.msg = status.msg || '';
    status.msg += ERROR_MESSAGES.FIELD.REQUIRED;
    status.required = false;
  }
  return status;
}

export { email };
