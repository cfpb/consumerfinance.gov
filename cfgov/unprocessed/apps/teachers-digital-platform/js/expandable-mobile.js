import ExpandableTransition from '@cfpb/cfpb-expandables/src/ExpandableTransition';

const MOBILE_COLLAPSED_SELECTOR = '.o-expandable__mobile-collapsed';
const MOBILE_WIDTH = 800;

/**
 * Alter DOM as necessary before cfpb-expandables ExpandableTransition.init()
 * so some elements won't be expanded by default.
 */
function beforeExpandableTransitionInit() {
  if ( window.innerWidth <= MOBILE_WIDTH ) {
    document.querySelectorAll( MOBILE_COLLAPSED_SELECTOR ).forEach( el => {
      el.classList.remove( ExpandableTransition.CLASSES.OPEN_DEFAULT );
    } );
  }
}

export default beforeExpandableTransitionInit;
