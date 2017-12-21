/* ==========================================================================
   Scripts for Feedback Form organism.
   ========================================================================== */


const COMMENT_ERRORS = require( '../../config/error-messages-config' ).COMMENT;
const OPTION_ERRORS = require( '../../config/error-messages-config' ).OPTION;
const FormSubmit = require( '../../organisms/FormSubmit.js' );
const BASE_CLASS = 'o-feedback';
let requiredKey = 'REQUIRED';
let UNDEFINED;
const element = document.body.querySelector( '.' + BASE_CLASS );

function validateFeedback( fields ) {
  if ( fields.comment ) {
    if ( fields.comment.value ) {
      return UNDEFINED;
    } else if ( fields.comment.hasAttribute( 'required' ) ) {
      return COMMENT_ERRORS[requiredKey];
    }
  }
  if ( fields.is_helpful ) {
    for ( let i = 0; i < fields.is_helpful.length; i++ ) {
      if ( fields.is_helpful[i].checked ) {
        return UNDEFINED;
      }
    }
    return OPTION_ERRORS[requiredKey];
  }
  return UNDEFINED;
}

if ( element ) {
  const replaceForm = element.getAttribute( 'data-replace' );
  const languageField = element.querySelector( 'input[name="language"]' );
  const language = languageField && languageField.value === 'es' ? 'es' : 'en';
  if ( language === 'es' ) {
    requiredKey = 'REQUIRED_ES';
  }

  const opts = {
    validator: validateFeedback,
    replaceForm:  replaceForm || language === 'es',
    minReplacementHeight: replaceForm,
    language: language
  };

  const formSubmit = new FormSubmit(
    element,
    BASE_CLASS,
    opts
  );

  formSubmit.init();
}
