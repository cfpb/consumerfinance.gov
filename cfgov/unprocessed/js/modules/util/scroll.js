'use strict';

var _requestAnimationFrame = window.requestAnimationFrame ||
    window.webkitRequestAnimationFrame ||
    window.mozRequestAnimationFrame ||
    function( callback ) {
      return setTimeout( function() {
        callback( Number( new Date() ) );
      },
    1000 / 60 ); };


/**
 * Easing
 * @param {Number} t current time
 * @param {Number} b start position
 * @param {Number} c difference between start and end position
 * @param {Number} d duration
 * @returns {Number} next position
 *
 */
function _easeInOutQuad( t, b, c, d ) {
  t /= d / 2;
  if ( t < 1 ) {
    return c / 2 * t * t + b;
  }
  t--;
  return -c / 2 * ( t * ( t - 2 ) - 1 ) + b;
}

/**
 * Calculate duration of scroll based on distance
 * @param {Number} distance The distance that will be scrolled
 * @returns {Number} scroll duration
 *
 */
function _calculateDuration( distance ) {
  var duration = Math.abs( distance ) / 2;
  return Math.min( Math.max( duration, 200 ), 500 ) || 200;
}

/**
 * Animated scroll to a location in page.
 * @param {Number} to The y-coordinate to scroll to
 * @param {Number} duration Duration of the scroll animation (optional)
 *
 */
function scrollTo( to, duration ) {
  var startPosition = window.scrollY;
  var distance = to - startPosition;
  var startTime;
  duration = _calculateDuration( distance );

  function scroll( timestamp ) {
    startTime = startTime || timestamp;
    var elapsed = timestamp - startTime;
    var next = _easeInOutQuad( elapsed, startPosition, distance, duration );
    window.scroll( 0, next );
    if ( elapsed < duration ) {
      _requestAnimationFrame( scroll );
    }
  }

  if ( Math.abs( distance ) > 3 ) {
    _requestAnimationFrame( scroll );
  }
}

/**
 * Checks whether element in viewport and if not,
 * scrolls it into view.
 * @param {HTMLNode} elem The DOM element to check for
 *
 */
function scrollIntoView( elem ) {
  if ( !elementInView( elem ) ) {
    var offset = elem.getBoundingClientRect().top;
    var to = window.pageYOffset + offset;
    scrollTo( to );
  }
}

/**
 * @param {HTMLNode} elem The DOM element to check for
 * @param {HTMLNode} strict If strict, whole element (or
 *    as much as will fit) must be in viewport
 * @returns {Boolean} Whether the element is in the viewport.
 */
function elementInView( elem, strict ) {
  var windowHeight = window.innerHeight;
  var windowTop = window.pageYOffset;
  var windowBottom = windowTop + windowHeight;
  var elementHeight = elem.offsetHeight;
  var elementTop = elem.getBoundingClientRect().top + windowTop;
  var elementBottom = elementTop + elementHeight;

  return elementBottom >= windowTop && elementTop <= windowBottom;
  // return: top in viewport and bottom also, or height is > than windowHeight
}


module.exports = {
  elementInView: elementInView,
  scrollIntoView: scrollIntoView,
  scrollTo: scrollTo
};
