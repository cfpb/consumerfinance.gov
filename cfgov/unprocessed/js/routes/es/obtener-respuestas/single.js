var Autocomplete = require( '../../../molecules/Autocomplete' );
require( '../../on-demand/feedback-form' );

var autocompleteContainer = document.querySelector( '.m-autocomplete' );
if ( autocompleteContainer ) {
	var autocomplete = new Autocomplete( autocompleteContainer, { 
		url: '/es/obtener-respuestas/api/autocomplete/?term='  
	} ).init();
}