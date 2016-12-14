/* ==========================================================================
   Scripts for Email Signup organism.
   ========================================================================== */

'use strict';

var FormSubmit = require( '../../organisms/FormSubmit.js' );
var validators = require( '../../modules/util/validators' );

var BASE_CLASS = 'o-email-signup';

function emailValidation ( fields ) {
  if ( fields.email && !fields.email.value ) {
  	return 'Please enter an email address.';
  } 
  return validators.email( fields.email ).msg;
}

var formSubmit = new FormSubmit(
  document.body.querySelector( '.' + BASE_CLASS ),
  BASE_CLASS,
  { validator: emailValidation }
);


formSubmit.init();
