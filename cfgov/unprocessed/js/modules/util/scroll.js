import { assign } from './assign';

const _requestAnimationFrame = window.requestAnimationFrame ||
    window.webkitRequestAnimationFrame ||
    window.mozRequestAnimationFrame ||
    function( callback ) {
      return setTimeout( function() {
        callback( Number( new Date() ) );
      }, 1000 / 60 );
    };

/**
 * Easing
 * @param {Number} currentTime current time
 * @param {Number} startPosition start position
 * @param {Number} distance difference between start and end position
 * @param {Number} duration duration
 * @returns {Number} next position
 *
 */
function _easeInOutQuad( currentTime, startPosition, distance, duration ) {
  let distanceDelta;
  const halfDuration = duration / 2;
  let updatedTime = currentTime / halfDuration;

  if ( updatedTime < 1 ) {
    distanceDelta = distance / 2 * updatedTime * updatedTime;
  } else {
    updatedTime--;
    // eslint-disable-next-line no-mixed-operators
    distanceDelta =
      -distance / 2 * ( updatedTime * ( updatedTime - 2 ) - 1 );
  }
  return distanceDelta + startPosition;
}

/**
 * Calculate duration of scroll based on distance
 * @param {Number} distance The distance that will be scrolled
 * @returns {Number} scroll duration
 *
 */
function _calculateDuration( distance ) {
  const duration = Math.abs( distance ) / 2;
  return Math.min( Math.max( duration, 200 ), 1000 ) || 500;
}

/**
 * Animated scroll to a location in page.
 * @param {Number} to The y-coordinate to scroll to
 * @param {Object} opts Optional parameters, including:
 *    duration: Duration of the scroll animation
 *    callback: To be called when scroll is complete
 *
 */
function scrollTo( to, opts ) {
  opts = opts && typeof opts === 'object' ? opts : {};
  const startPosition = window.pageYOffset;
  const distance = to - startPosition;
  const duration = opts.duration || _calculateDuration( distance );
  let startTime;

  /**
   * Scroll the window for the duration
   * Trigger a callback after the duration has ended
   * @param {Number} timestamp - the current time returned by
   *    requestAnimationFrame
   */
  function scroll( timestamp ) {
    startTime = startTime || timestamp;
    const elapsed = timestamp - startTime;
    const next =
      _easeInOutQuad( elapsed, startPosition, distance, duration );
    window.scroll( 0, next );

    if ( elapsed < duration ) {
      _requestAnimationFrame( scroll );
    } else if ( typeof opts.callback === 'function' ) {
      opts.callback();
    }
  }

  if ( Math.abs( distance ) > 3 ) {
    _requestAnimationFrame( scroll );
  } else if ( typeof opts.callback === 'function' ) {
    opts.callback();
  }
}

/**
 * Checks whether element in viewport and if not,
 * scrolls it into view.
 * @param {HTMLNode} elem The DOM element to check for
 * @param {Object} opts Optional parameters, including:
 *  offset: Distance from top of screen of element when scroll is complete.
 *  callback: function called when scroll is complete.
 *
 */
function scrollIntoView( elem, opts ) {
  const defaults = { offset: 15 };
  opts = assign( defaults, opts );
  if ( !elementInView( elem, true ) ) {
    const elementTop = elem.getBoundingClientRect().top;
    const to = Math.max(
      window.pageYOffset + elementTop - opts.offset, 0
    );
    scrollTo( to, opts );
  } else if ( opts.callback && typeof opts.callback === 'function' ) {
    opts.callback();
  }
}

/**
 * @param {HTMLNode} elem The DOM element to check for
 * @param {Boolean} strict Tests whether whole element is
 * onscreen rather than just a part.
 * @returns {Boolean} Whether the element is in the viewport.
 */
function elementInView( elem, strict ) {
  const windowHeight = window.innerHeight;
  const windowTop = window.pageYOffset;
  const windowBottom = windowTop + windowHeight;
  const elementHeight = elem.offsetHeight;
  const elementTop = elem.getBoundingClientRect().top + windowTop;
  const elementBottom = elementTop + elementHeight;

  if ( strict ) {
    return elementTop >= windowTop && elementBottom <= windowBottom;
  }
  return elementBottom >= windowTop && elementTop <= windowBottom;
}

window.scrollToElement = scrollTo;

export {
  elementInView,
  scrollIntoView,
  scrollTo
};
