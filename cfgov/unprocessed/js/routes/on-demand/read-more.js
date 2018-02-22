const Expandable = require( '../../organisms/Expandable' );
const getBreakpointState = require( '../../modules/util/breakpoint-state' ).get;

const readMoreContainers = document.querySelectorAll( '.o-expandable__read-more' );

if ( readMoreContainers && getBreakpointState().isBpXS ) {
  for ( let i = 0; i < readMoreContainers.length; i++ ) {
    const container = readMoreContainers[i];
    const readMoreExpandable = new Expandable( container ).init();
    readMoreExpandable.addEventListener( 'expandEnd', function() {
      readMoreExpandable.destroy();
      container.querySelector( '.o-expandable_content' ).style.height = '';
    } );
  }
}

