var Autocomplete = require( '../../molecules/Autocomplete' );

var autocompleteContainer = document.querySelector( '.m-autocomplete' );
console.log(autocompleteContainer)
if ( autocompleteContainer ) {
	var autocomplete = new Autocomplete( autocompleteContainer, { 
		url: '/ask-cfpb/api/autocomplete/?term=' 
	} ).init();
}
