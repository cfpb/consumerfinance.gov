/* ==========================================================================
   Scripts for Feedback Form organism.
   ========================================================================== */

'use strict';

var messages = {
	'en' : {
		'comment': "Please enter a comment.",
		'option': 'Please select an option.'

	},
	'es': {
		'comment': "Por favor, introduzca un comentario.",
		'option': 'Por favor, seleccione una opción.'
	}
}

var FormSubmit = require( '../../organisms/FormSubmit.js' );

var BASE_CLASS = 'o-feedback';

var element = document.body.querySelector( '.' + BASE_CLASS );

if ( element ) {
	var languageField = element.querySelector('input[name="language"]');
	var language = languageField && languageField.value === 'es' ? 'es' : 'en';
	var replaceForm = element.getAttribute('data-replace');

	var opts = {
	  validator: validateFeedback, 
	  replaceForm:  replaceForm || language === 'es',
	  minReplacementHeight: replaceForm,
	  language: language
	}

	function validateFeedback( fields ) {
		if ( fields.comment ) {
			if ( fields.comment.value ) {
				return;
			} else if ( fields.comment.hasAttribute('required') ) {
				return messages[language]['comment'];
			} 
		} 
		if ( fields['is_helpful'] ) {
			for ( var i = 0; i < fields['is_helpful'].length; i ++ ) {
				if ( fields['is_helpful'][i].checked ) {
					return;
				}
			}
			return messages[language]['option'];
		}
	}

	var formSubmit = new FormSubmit(
	  element,
	  BASE_CLASS,
	  opts
	);

	formSubmit.init();
}

