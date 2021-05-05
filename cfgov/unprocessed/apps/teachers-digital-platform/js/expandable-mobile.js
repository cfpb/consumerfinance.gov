import ExpandableTransition from '@cfpb/cfpb-expandables/src/ExpandableTransition';

const MOBILE_COLLAPSED_CLASS = 'o-expandable__mobile-collapsed';
const MOBILE_WIDTH = 800;

let innerWidth;

function getInnerWidth() {
  return innerWidth || window.innerWidth;
}

// For unit tests
function setInnerWidth(width) {
  innerWidth = width;
}

/**
 * Alter DOM as necessary before cfpb-expandables ExpandableTransition.init()
 * so some elements won't be expanded by default.
 */
function beforeExpandableTransitionInit() {
  document.querySelectorAll( '.' + MOBILE_COLLAPSED_CLASS ).forEach( el => {
    if ( getInnerWidth() <= MOBILE_WIDTH ) {
      el.classList.remove( ExpandableTransition.CLASSES.OPEN_DEFAULT );
    }

    // Always clean up this class, just used at init time
    el.classList.remove( MOBILE_COLLAPSED_CLASS );
  } );
}

export { setInnerWidth, MOBILE_COLLAPSED_CLASS };

export default beforeExpandableTransitionInit;
