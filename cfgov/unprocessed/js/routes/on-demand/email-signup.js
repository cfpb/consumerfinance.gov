/* ==========================================================================
   Scripts for Email Signup organism.
   ========================================================================== */

'use strict';

var FormSubmit = require( '../../organisms/FormSubmit.js' );
var validators = require( '../../modules/util/validators' );

var BASE_CLASS = 'o-email-signup';
var language = document.body.querySelector( '.content' ).lang;

function emailValidation ( fields ) {
  return validators.email(
  	fields.email,
  	'',
  	{ language: language }
  ).msg;
}

var formSubmit = new FormSubmit(
  document.body.querySelector( '.' + BASE_CLASS ),
  BASE_CLASS,
  { validator: emailValidation, language: language }
);

formSubmit.init();
