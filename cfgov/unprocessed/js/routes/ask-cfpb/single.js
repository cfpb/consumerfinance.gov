require( '../on-demand/ask-autocomplete' );

var Expandable = require( '../../organisms/Expandable' );
var getBreakpointState = require( '../../modules/util/breakpoint-state' ).get;

var readMoreContainer = document.querySelector( '.o-expandable__read-more' );
if ( readMoreContainer && getBreakpointState().isBpXS ) {
	var readMoreExpandable = new Expandable( readMoreContainer ).init();
	readMoreExpandable.addEventListener( 'expandEnd', function () {
		readMoreExpandable.destroy();
		readMoreContainer.querySelector( '.o-expandable_content' ).style.height = '';
	} );
}
