/* ==========================================================================
   Scripts for Feedback Form organism.
   ========================================================================== */

'use strict';

var FormSubmit = require( '../../organisms/FormSubmit.js' );

var BASE_CLASS = 'o-feedback';

function validateFeedback( fields ) {
	if ( fields.comment && !fields.comment.value ) {
		return "Please enter a comment."
	}
}

var formSubmit = new FormSubmit(
  document.body.querySelector( '.' + BASE_CLASS ),
  BASE_CLASS,
  validateFeedback
);

formSubmit.init();