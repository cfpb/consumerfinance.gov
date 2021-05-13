import ExpandableTransition from '@cfpb/cfpb-expandables/src/ExpandableTransition';

const MOBILE_COLLAPSED_CLASS = 'o-expandable__mobile-collapsed';
const MOBILE_WIDTH = 800;

let innerWidth;

/**
 * Get the viewport width
 *
 * @returns {number} The viewport width
 */
function getInnerWidth() {
  return innerWidth || window.innerWidth;
}

/**
 * Fix the output of getInnerWidth() for test purposes
 *
 * @param {number} width Width
 */
function setInnerWidth( width ) {
  innerWidth = width;
}

/**
 * Alter DOM as necessary before cfpb-expandables ExpandableTransition.init()
 * so some elements won't be expanded by default.
 */
function beforeExpandableTransitionInit() {
  const nodeList = document.querySelectorAll( '.' + MOBILE_COLLAPSED_CLASS );

  // IE11 lacks NodeList.forEach
  [].forEach.call( nodeList, el => {
    if ( getInnerWidth() <= MOBILE_WIDTH ) {
      el.classList.remove( ExpandableTransition.CLASSES.OPEN_DEFAULT );
    }

    // Always clean up this class, just used at init time
    el.classList.remove( MOBILE_COLLAPSED_CLASS );
  } );
}

export { setInnerWidth, MOBILE_COLLAPSED_CLASS };

export default beforeExpandableTransitionInit;
