/* ==========================================================================
   Scripts for Feedback Form organism.
   ========================================================================== */

'use strict';

var FormSubmit = require( '../../organisms/FormSubmit.js' );

var BASE_CLASS = 'o-feedback';

function validateFeedback( fields ) {

	if ( fields.comment ) {
		if ( fields.comment.value ) {
			return;
		} else if ( fields.comment.hasAttribute('required') ) {
			if ( fields.language == 'es' ) {
				return "Por favor, introduzca un comentario."
			}
			return "Please enter a comment."
		} 
	} 
	if ( fields['is_helpful'] ) {
		for ( var i = 0; i < fields['is_helpful'].length; i ++ ) {
			if ( fields['is_helpful'][i].checked ) {
				return;
			}
		}
		if ( fields.language == 'es' ) {
			return 'Por favor, seleccione una opción.'
		}
		return 'Please select an option.'
	}
}

var element = document.body.querySelector( '.' + BASE_CLASS );

if (element )

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