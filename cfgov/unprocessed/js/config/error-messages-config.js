/* ==========================================================================
  Error Messages Config

  These messages are manually mirrored on the Python side in config.py
   ========================================================================== */

'use strict';

var ERROR_MESSAGES = {
  CHECKBOX_ERRORS: {
    required: 'Please select at least one of the "%s" options.'
  },
  DATE_ERRORS: {
    invalid:      'You have entered an invalid date.',
    one_required: 'Please enter at least one date.'
  }
};

module.exports = ERROR_MESSAGES;
