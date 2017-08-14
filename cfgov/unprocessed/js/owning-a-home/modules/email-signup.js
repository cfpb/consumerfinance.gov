'use strict';

const FormSubmit = require( '../../organisms/FormSubmit.js' );
const validators = require( '../../modules/util/validators' );
const BASE_CLASS = 'o-email-signup';
const baseElement = document.body.querySelector( '.' + BASE_CLASS );

function emailValidation( fields ) {
  if ( fields.email && !fields.email.value ) {
    return 'Please enter an email address.';
  }
  return validators.email( fields.email ).msg;
}

if ( baseElement ) {
  var formSubmit = new FormSubmit(
    baseElement,
    BASE_CLASS,
    { validator: emailValidation }
  );

  formSubmit.init();
}
