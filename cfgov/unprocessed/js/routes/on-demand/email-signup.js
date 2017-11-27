/* ==========================================================================
   Scripts for Email Signup organism.
   ========================================================================== */

'use strict';

var FormSubmit = require( '../../organisms/FormSubmit.js' );
var validators = require( '../../modules/util/validators' );

var BASE_CLASS = 'o-email-signup';
var language = document.body.querySelector( '.content' ).lang;
var emailSignUps = document.body.querySelectorAll( '.' + BASE_CLASS )
var emailSignUpsLength = emailSignUps.length;
var formSubmit;

function emailValidation ( fields ) {
  return validators.email(
    fields.email,
    '',
    { language: language }
  ).msg;
}

for ( var i = 0; i < emailSignUpsLength; i++ ) {
  formSubmit = new FormSubmit(
    emailSignUps[i],
    BASE_CLASS,
    { validator: emailValidation, language: language }
  );

  formSubmit.init();
}
