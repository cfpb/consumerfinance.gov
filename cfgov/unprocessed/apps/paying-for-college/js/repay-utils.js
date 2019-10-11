// Utilities to help repay.js work

const hide = function( haystack, selector ) {
  if ( typeof selector === 'undefined' ) {
    haystack.style.display = 'none';
  } else {
    haystack.querySelectorAll( selector ).forEach( elem => {
      elem.style.display = 'none';
    } );
  }
};

const show = function( haystack, selector ) {
  if ( typeof selector === 'undefined' ) {
    haystack.style.display = 'block';
  } else {
    haystack.querySelectorAll( selector ).forEach( elem => {
      elem.style.display = 'block';
    } );
  }

};

const getElementHeight = function( elem ) {
  const style = window.getComputedStyle( elem );
  const display = style.display;
  const position = style.position;
  const visibility = style.visibility;
  const maxHeight = style.maxHeight;
  let height = 0;

  // An invisible block element has the height and stuff we're looking for.
  elem.style.position = 'absolute';
  elem.style.visibility = 'hidden';
  elem.style.display = 'block';
  elem.style.maxHeight = null;

  height = elem.offsetHeight;

  elem.style.position = position;
  elem.style.display = display;
  elem.style.visibility = visibility;
  elem.style.maxHeight = maxHeight;

  return height;
};

const slide = function( direction, elem, callback ) {
  if ( elem === null ) {
    // console.log( 'ERR: null element passed to slide.' );
    return;
  }
  let newHeight = '0';
  if ( direction === 'up' ) {
    elem.style.overflowY = 'hidden';
  } else if ( direction === 'down' ) {
    newHeight = getElementHeight( elem );
    elem.style.overflowY = null;
    elem.style.maxHeight = '0px';
  }

  newHeight += 'px';

  elem.style.display = 'block';
  elem.style.transition = 'max-height 0.5s ease-in-out';

  setTimeout( () => {
    elem.style.maxHeight = newHeight;
    if ( direction === 'up' ) {
      setTimeout( () => {
        elem.style.display = 'none';
      }, 510 );
    } else {
      setTimeout( () => {
        elem.style.maxHeight = null;
      }, 510 );
    }
  }, 10 );

};

const isVisible = function( element ) {
  if ( element.style.display === 'none' ) {
    return false;
  }
  return Boolean( element.offsetWidth && element.offsetHeight && element.getClientRects().length );
};

/**
 * scrollY - Get the Y coord of the current viewport. Older browsers don't
 * support `scrollY` so use whichever works.
 *
 * @returns {function} Browser-supported y offset method.
 */
const scrollY = () => window.scrollY || window.pageYOffset;

/**
 * getYLocation - Get Y location of provided element on the page.
 *
 * @param {node} el HTML element
 *
 * @returns {type} Description
 */
const getYLocation = el => {
  const elOffset = el.getBoundingClientRect().top;
  return scrollY() + elOffset;
};

module.exports = {
  hide,
  show,
  getElementHeight,
  slide,
  isVisible,
  getYLocation
};
