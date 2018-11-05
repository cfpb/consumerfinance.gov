/* ==========================================================================
   Scripts for Feedback Form organism.
   ========================================================================== */

<<<<<<< HEAD
import ERROR_MESSAGES from '../../config/error-messages-config';
=======
import { COMMENT, OPTION } from '../../config/error-messages-config';
>>>>>>> Convert JS to use ES6 modules
import FormSubmit from '../../organisms/FormSubmit.js';

const BASE_CLASS = 'o-feedback';
let requiredKey = 'REQUIRED';
let UNDEFINED;
const element = document.body.querySelector( '.' + BASE_CLASS );

function validateFeedback( fields ) {
  if ( fields.comment ) {
    if ( fields.comment.value ) {
      return UNDEFINED;
    } else if ( fields.comment.hasAttribute( 'required' ) ) {
<<<<<<< HEAD
      return ERROR_MESSAGES.COMMENT[requiredKey];
=======
      return COMMENT[requiredKey];
>>>>>>> Convert JS to use ES6 modules
    }
  }
  if ( fields.is_helpful ) {
    for ( let i = 0; i < fields.is_helpful.length; i++ ) {
      if ( fields.is_helpful[i].checked ) {
        return UNDEFINED;
      }
    }
<<<<<<< HEAD
    return ERROR_MESSAGES.OPTION[requiredKey];
=======
    return OPTION[requiredKey];
>>>>>>> Convert JS to use ES6 modules
  }
  return UNDEFINED;
}

if ( element ) {
  const languageField = element.querySelector( 'input[name="language"]' );
  const language = languageField && languageField.value === 'es' ? 'es' : 'en';
  if ( language === 'es' ) {
    requiredKey = 'REQUIRED_ES';
  }

  const opts = {
    validator: validateFeedback,
    replaceForm:  true,
    language: language
  };

  const formSubmit = new FormSubmit(
    element,
    BASE_CLASS,
    opts
  );

  formSubmit.init();
}
