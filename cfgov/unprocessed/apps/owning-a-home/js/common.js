/* ==========================================================================
   Common application-wide scripts for owning-a-home.
   ========================================================================== */

import { email as validateEmail } from '../../../js/modules/util/validators.js';
import FormSubmit from '../../../js/organisms/FormSubmit.js';

const BASE_CLASS = 'o-email-signup';
const emailSignup = document.body.querySelector('.' + BASE_CLASS);

if (emailSignup) {
  const language = document.documentElement.lang || 'en';
  const formSubmit = new FormSubmit(emailSignup, BASE_CLASS, {
    validator: (fields) =>
      validateEmail(fields.email, '', { language: language }).msg,
    language: language,
  });

  formSubmit.init();
}
