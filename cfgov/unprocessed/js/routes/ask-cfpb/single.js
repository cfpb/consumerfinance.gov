var Autocomplete = require( '../../molecules/Autocomplete' );
var Expandable = require( '../../organisms/Expandable' );
var getBreakpointState = require( '../../modules/util/breakpoint-state' ).get;

var autocompleteContainer = document.querySelector( '.m-autocomplete' );
if ( autocompleteContainer ) {
	var autocomplete = new Autocomplete( autocompleteContainer, { 
		url: '/ask-cfpb/api/autocomplete/?term=' 
	} ).init();
}

var readMoreContainer = document.querySelector( '.o-expandable__read-more' );
if ( readMoreContainer && getBreakpointState().isBpXS ) {
	var readMoreExpandable = new Expandable( readMoreContainer ).init();
	readMoreExpandable.addEventListener( 'expandEnd', function () {
		readMoreExpandable.destroy();
		element.querySelector( '.o-expandable_content' ).style.height = '';
	} );
}
