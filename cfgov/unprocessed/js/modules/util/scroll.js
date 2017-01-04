'use strict';
var assign = require( './assign' ).assign;

var _requestAnimationFrame = window.requestAnimationFrame ||
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
  currentTime /= duration / 2;
  if ( currentTime < 1 ) {
    return distance / 2 * currentTime * currentTime + startPosition;
  }
  currentTime--;
  return -distance / 2 * ( currentTime * ( currentTime - 2 ) - 1 ) + startPosition;
}

/**
 * Calculate duration of scroll based on distance
 * @param {Number} distance The distance that will be scrolled
 * @returns {Number} scroll duration
 *
 */
function _calculateDuration( distance ) {
  var duration = Math.abs( distance ) / 2;
  return Math.min( Math.max( duration, 200 ), 1000 ) || 500;
}

/**
 * Animated scroll to a location in page.
 * @param {Number} to The y-coordinate to scroll to
 * @param {Object} opts Optional parameters, including:
 * 		duration: Duration of the scroll animation
 * 		callback: To be called when scroll is complete
 *
 */
function scrollTo( to, opts ) {
  opts = opts && typeof opts === 'object' ? opts : {};
  var startPosition = window.pageYOffset;
  var distance = to - startPosition;
  var duration = opts.duration || _calculateDuration( distance );
  var startTime;

  function scroll( timestamp ) {
    startTime = startTime || timestamp;
    var elapsed = timestamp - startTime;
    var next = _easeInOutQuad( elapsed, startPosition, distance, duration );
    window.scroll( 0, next );
    if ( elapsed < duration ) {
      _requestAnimationFrame( scroll );
    } else if ( typeof opts.callback === 'function' ) {
      opts.callback();
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
 * @param {Object} opts Optional parameters, including:
 * 	  offset: Distance from top of screen of element
        when scroll is complete
 *    callback: function called when scroll is complete
 *
 */
function scrollIntoView( elem, opts ) {
  var defaults = { offset: 15 };
  opts = assign( defaults, opts );
  if ( !elementInView( elem, true ) ) {
    var elementTop = elem.getBoundingClientRect().top;
    var to = Math.max( window.pageYOffset + elementTop - opts.offset, 0 );
    scrollTo( to, opts );
  }
}

/**
 * @param {HTMLNode} elem The DOM element to check for
 * @param {Boolean} strict Tests whether whole element is
 * onscreen rather than just a part.
 * @returns {Boolean} Whether the element is in the viewport.
 */
function elementInView( elem, strict ) {
  var windowHeight = window.innerHeight;
  var windowTop = window.pageYOffset;
  var windowBottom = windowTop + windowHeight;
  var elementHeight = elem.offsetHeight;
  var elementTop = elem.getBoundingClientRect().top + windowTop;
  var elementBottom = elementTop + elementHeight;

  if ( strict ) {
    return elementTop >= windowTop && elementBottom <= windowBottom;
  }
  return elementBottom >= windowTop && elementTop <= windowBottom;
}


module.exports = {
  elementInView: elementInView,
  scrollIntoView: scrollIntoView,
  scrollTo: scrollTo
};

window.scrollToElement = scrollTo;

