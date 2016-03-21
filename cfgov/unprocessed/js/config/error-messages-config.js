/* ==========================================================================
  Error Messages Config

  These messages are manually mirrored on the Python side in config.py
   ========================================================================== */

'use strict';

var ERROR_MESSAGES = {
  CHECKBOX: {
    REQUIRED: 'Please select at least %s of the options.'
  },
  DATE: {
    INVALID: 'You have entered an invalid date.',
    ONE_REQUIRED: 'Please enter at least one date.'
  },
  EMAIL: {
    INVALID: 'You have entered an invalid email address.',
    REQUIRED: 'Please enter an email address.'
  },
  FIELD: {
    REQUIRED: 'This field is required.'
  },
  DEFAULT: 'Error!',
  DOM: {
    INVALID: 'Invalid dom element was provided.'
  }
};

module.exports = Object.freeze( ERROR_MESSAGES );
