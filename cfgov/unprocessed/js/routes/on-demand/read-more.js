const Expandable = require( '../../organisms/Expandable' );
const getBreakpointState = require( '../../modules/util/breakpoint-state' ).get;

const readMoreContainer = document.querySelector( '.o-expandable__read-more' );
if ( readMoreContainer && getBreakpointState().isBpXS ) {
  const readMoreExpandable = new Expandable( readMoreContainer ).init();
  readMoreExpandable.addEventListener( 'expandEnd', function() {
    readMoreExpandable.destroy();
    readMoreContainer.querySelector( '.o-expandable_content' ).style.height = '';
  } );
}