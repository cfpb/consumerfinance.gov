'use strict';

var $ = window.$;

/**
 * Stores/retrieves email signup data in localStorage
 */

var POPUP_WAIT_PERIOD = [ 4, 30, 60 ];
var DISPLAY_DATE_KEY = 'oahPopupShowNext';
var DISPLAY_COUNT_KEY = 'oahPopupCount';
var FOREVER = 10000;

function getFutureDate( days ) {
  var date = new Date();
  return date.setTime( date.getTime() + ( days * 24 * 60 * 60 * 1000 ) );
}

function recordEmailPopupView() {
  var count = Number( localStorage.getItem( DISPLAY_COUNT_KEY ) ) || 0;
  var max = POPUP_WAIT_PERIOD.length - 1;
  count = count >= max ? max : count;
  var days = POPUP_WAIT_PERIOD[count];
  localStorage.setItem( DISPLAY_COUNT_KEY, count + 1 );
  localStorage.setItem( DISPLAY_DATE_KEY, getFutureDate( days ) );
}

function recordEmailPopupClosure() {
  var count = POPUP_WAIT_PERIOD.length - 1;
  var days = POPUP_WAIT_PERIOD[count];
  localStorage.setItem( DISPLAY_COUNT_KEY, count );
  localStorage.setItem( DISPLAY_DATE_KEY, getFutureDate( days ) );
}

function recordEmailRegistration() {
  localStorage.setItem( DISPLAY_DATE_KEY, getFutureDate( FOREVER ) );
}

function showEmailPopup() {
  var today = new Date().getTime();
  var nextDisplayDate = Number( localStorage.getItem( DISPLAY_DATE_KEY ) ) || 0;
  return today > nextDisplayDate;
}

function _throttle( func, wait, options ) {
  var context, args, result;
  var timeout = null;
  var previous = 0;
  if ( !options ) options = {};
  var later = function() {
    previous = options.leading === !1 ? 0 : Date.now();
    timeout = null;
    result = func.apply( context, args );
    if ( !timeout ) context = args = null;
  };
  return function() {
    var now = Date.now();
    if ( !previous && options.leading === !1 ) previous = now;
    var remaining = wait - ( now - previous );
    context = this;
    args = arguments;
    if ( remaining <= 0 || remaining > wait ) {
      if ( timeout ) {
        clearTimeout( timeout );
        timeout = null;
      }
      previous = now;
      result = func.apply( context, args );
      if ( !timeout ) context = args = null;
    } else if ( !timeout && options.trailing !== !1 ) {
      timeout = setTimeout( later, remaining );
    }
    return result;
  };
}

function showOnScroll( elToShow, opts ) {
  var UNDEFINED;
  var defaults = {
    scrollPercent: 50,
    throttleDelay: 10,
    targetElement: null,
    cb: function() { return UNDEFINED; }
  };

  opts = $.extend( defaults, opts || {} );

  function _getScrollTargetPosition() {
    var elHeight = elToShow.height();
    if ( opts.targetElement && opts.targetElement.length ) {
      var top = opts.targetElement.offset().top;
      return top + elHeight;
    }
    var percentageTarget = $( document ).height() * ( opts.scrollPercent / 100 );
    return percentageTarget + elHeight;

  }

  function _scrollTargetPositionReached() {
    var windowHeight = window.innerHeight;
    var windowTop = window.pageYOffset;
    var windowBottom = windowTop + windowHeight;
    var scrollTargetPosition = _getScrollTargetPosition();
    return windowBottom > scrollTargetPosition;
  }

  var handler = _throttle( function( event ) {
    if ( _scrollTargetPositionReached() ) {
      window.removeEventListener( 'scroll', handler );
      if ( typeof opts.cb === 'function' ) {
        opts.cb();
      }
    }
  }, opts.throttleDelay );

  window.addEventListener( 'scroll', handler );
}

module.exports = {
  showEmailPopup: showEmailPopup,
  recordEmailPopupView: recordEmailPopupView,
  recordEmailRegistration: recordEmailRegistration,
  recordEmailPopupClosure: recordEmailPopupClosure,
  showOnScroll: showOnScroll
};
