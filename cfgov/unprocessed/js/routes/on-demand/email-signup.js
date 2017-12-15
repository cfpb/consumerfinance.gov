/* ==========================================================================
   Scripts for Email Signup organism.
   ========================================================================== */


const FormSubmit = require( '../../organisms/FormSubmit.js' );
const validators = require( '../../modules/util/validators' );

const BASE_CLASS = 'o-email-signup';
const language = document.body.querySelector( '.content' ).lang;
const emailSignUps = document.body.querySelectorAll( '.' + BASE_CLASS );
const emailSignUpsLength = emailSignUps.length;
let formSubmit;

function emailValidation( fields ) {
  return validators.email(
    fields.email,
    '',
    { language: language }
  ).msg;
}

for ( let i = 0; i < emailSignUpsLength; i++ ) {
  formSubmit = new FormSubmit(
    emailSignUps[i],
    BASE_CLASS,
    { validator: emailValidation, language: language }
  );

  formSubmit.init();
}
