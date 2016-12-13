/* ==========================================================================
   Scripts for Feedback Form organism.
   ========================================================================== */

'use strict';

var FormSubmit = require( '../../organisms/FormSubmit.js' );

var BASE_CLASS = 'o-feedback';

function validateFeedback( fields ) {
	if ( fields.comment && fields.comment.hasAttribute('required') && !fields.comment.value ) {
		return "Please enter a comment."
	} else if ( fields['is_helpful'] ) {
		for ( var i = 0; i < fields['is_helpful'].length; i ++ ) {
			if ( fields['is_helpful'][i].checked ) {
				return;
			}
		}
		return 'Please select an option.'
	}
}

var element = document.body.querySelector( '.' + BASE_CLASS );

var opts = {
  validator: validateFeedback, 
  replaceForm: element.getAttribute('data-replace')
 }

var formSubmit = new FormSubmit(
  element,
  BASE_CLASS,
  opts
);

formSubmit.init();