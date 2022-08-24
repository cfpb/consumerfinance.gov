/* ==========================================================================
   Scripts for Email Signup organism.
   ========================================================================== */

import * as validators from '../../modules/util/validators';
import FormSubmit from '../../organisms/FormSubmit.js';

const BASE_CLASS = 'o-email-signup';
const language = document.body.querySelector( '.content' ).lang;
const emailSignUps = document.body.querySelectorAll( '.' + BASE_CLASS );
const emailSignUpsLength = emailSignUps.length;
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


for ( let i = 0; i < emailSignUpsLength; i++ ) {
  const signup = emailSignUps[i];
  const form = signup.querySelector( 'form' );
  if ( form ) {
    formSubmit = new FormSubmit(
      signup,
      BASE_CLASS,
      { validator: emailValidation, language: language }
    );

    formSubmit.init();
  }
}
