/* ==========================================================================
   Scripts for Email Signup organism.
   ========================================================================== */

import { email as validateEmail } from '../../modules/util/validators.js';
import FormSubmit from '../../organisms/FormSubmit.js';

const BASE_CLASS = 'o-email-signup';
const language = document.documentElement.lang || 'en';
const emailSignUps = document.body.querySelectorAll('.' + BASE_CLASS);
const emailSignUpsLength = emailSignUps.length;
let formSubmit;

/**
 * @param {object} fields - Map of field options to validate.
 * @returns {string} The validator's message.
 */
function emailValidation(fields) {
  return validateEmail(fields.email, '', { language: language }).msg;
}

for (let i = 0; i < emailSignUpsLength; i++) {
  const signup = emailSignUps[i];
  const form = signup.querySelector('form');
  if (form) {
    formSubmit = new FormSubmit(signup, BASE_CLASS, {
      validator: emailValidation,
      language: language,
    });

    formSubmit.init();
  }
}
