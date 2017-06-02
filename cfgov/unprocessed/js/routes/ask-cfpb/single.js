var Expandable = require( '../../organisms/Expandable' );
var getBreakpointState = require( '../../modules/util/breakpoint-state' ).get;

var element = document.querySelector( '.o-expandable__read-more' );

if ( element && getBreakpointState().isBpXS ) {
	var readMoreExpandable = new Expandable( element ).init();
	readMoreExpandable.addEventListener( 'expandEnd', function () {
		readMoreExpandable.destroy();
		element.querySelector( '.o-expandable_content' ).style.height = '';
	} );
}
