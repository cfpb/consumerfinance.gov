/* ==========================================================================
   Scripts for Feedback Form organism.
   ========================================================================== */

'use strict';

var COMMENT_ERRORS = require( '../../config/error-messages-config' ).COMMENT || {};
var OPTION_ERRORS = require( '../../config/error-messages-config' ).OPTION || {};
var FormSubmit = require( '../../organisms/FormSubmit.js' );
var BASE_CLASS = 'o-feedback';
var requiredKey = 'REQUIRED';
var UNDEFINED;
var element = document.body.querySelector( '.' + BASE_CLASS );

function validateFeedback( fields ) {
  if ( fields.comment ) {
    if ( fields.comment.value ) {
      return UNDEFINED;
    } else if ( fields.comment.hasAttribute( 'required' ) ) {
      return COMMENT_ERRORS[requiredKey];
    }
  }
  if ( fields.is_helpful ) {
    for ( var i = 0; i < fields.is_helpful.length; i++ ) {
      if ( fields.is_helpful[i].checked ) {
        return UNDEFINED;
      }
    }
    return OPTION_ERRORS[requiredKey];
  }
  return UNDEFINED;
}

if ( element ) {
  var languageField = element.querySelector( 'input[name="language"]' );
  var language = languageField && languageField.value === 'es' ? 'es' : 'en';
  if ( language === 'es' ) {
    requiredKey = 'REQUIRED_ES';
  }

  var opts = {
    validator: validateFeedback,
    replaceForm:  true,
    language: language
  };

  var formSubmit = new FormSubmit(
    element,
    BASE_CLASS,
    opts
  );

  formSubmit.init();
}
