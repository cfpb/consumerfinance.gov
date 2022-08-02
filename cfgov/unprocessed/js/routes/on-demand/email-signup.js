/* ==========================================================================
   Scripts for Email Signup organism.
   ========================================================================== */

import * as validators from '../../modules/util/validators';
import FormSubmit from '../../organisms/FormSubmit.js';

const BASE_CLASS = 'o-email-signup';
const FORM_CLASS = 'o-form__email-signup';
const language = document.body.querySelector( '.content' ).lang;
const emailSignUps = document.body.querySelectorAll( '.' + BASE_CLASS );
const emailSignUpsForms = document.body.querySelectorAll( '.' + FORM_CLASS );
const emailSignUpsLength = emailSignUps.length;
const emailSignUpsFormsLength = emailSignUpsForms.length;
let formSubmit;

/**
 * @param {Object} fields - Map of field options to validate.
 * @returns {string} The validator's message.
 */
function emailValidation( fields ) {
  return validators.email(
    fields.email,
    '',
    { language: language }
  ).msg;
}

/* TODO: See if we can get rid of this by not including this JS on a page with
a link-only signup. If not, see if this can be refactored to be cleaner. */
if ( emailSignUpsFormsLength > 0 ) {
  for ( let i = 0; i < emailSignUpsLength; i++ ) {
    formSubmit = new FormSubmit(
      emailSignUps[i],
      BASE_CLASS,
      { validator: emailValidation, language: language }
    );

    formSubmit.init();
  }
}
