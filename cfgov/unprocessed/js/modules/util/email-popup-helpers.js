const _assign = require( './assign' ).assign;


/**
 * Stores/retrieves email signup data in localStorage
 *
 * After the first time a user sees a popup, the popup won't be displayed for
 * another 4 days. After the second time, it'll be another 30 days, then 60
 * days. If the user closes the popup, it'll reappear every 60 days.
 *
 * Submission of an email address dismisses the popup permanently.
 */

const POPUP_WAIT_PERIOD = [ 4, 30, 60 ];
const FOREVER = 10000;

/**
 * @param {string} popupLabel - label for this popup.
 * @returns {string} Local storage key to count popup views.
 */
function _getCountKey( popupLabel ) {
  return popupLabel + 'PopupCount';
}

/**
 * @param {string} popupLabel - label for this popup.
 * @returns {string} Local storage key to record next time to show popup.
 */
function _getNextShowKey( popupLabel ) {
  return popupLabel + 'PopupShowNext';
}

/**
 * @param {number} days - The number of days to a future date.
 * @returns {Date} A future date x amount of days from now.
 */
function _getFutureDate( days ) {
  const date = new Date();
  return date.setTime( date.getTime() + ( days * 24 * 60 * 60 * 1000 ) );
}

/**
 * Record in local storage that the email popup has been viewed.
 * @param {string} popupLabel - label for this popup.
 */
function recordEmailPopupView( popupLabel ) {
  const countKey = _getCountKey( popupLabel );
  const nextShowKey = _getNextShowKey( popupLabel );

  let count = Number( localStorage.getItem( countKey ) ) || 0;
  const max = POPUP_WAIT_PERIOD.length - 1;
  count = count >= max ? max : count;
  const days = POPUP_WAIT_PERIOD[count];
  localStorage.setItem( countKey, count + 1 );
  localStorage.setItem( nextShowKey, _getFutureDate( days ) );
}

/**
 * Record in local storage that the email popup has been closed.
 * @param {string} popupLabel - label for this popup.
 */
function recordEmailPopupClosure( popupLabel ) {
  const countKey = _getCountKey( popupLabel );
  const nextShowKey = _getNextShowKey( popupLabel );

  const count = POPUP_WAIT_PERIOD.length - 1;
  const days = POPUP_WAIT_PERIOD[count];
  localStorage.setItem( countKey, count );
  localStorage.setItem( nextShowKey, _getFutureDate( days ) );
}

/**
 * Sets email popup key in local storage with a very long expiry date.
 * @param {string} popupLabel - label for this popup.
 */
function recordEmailRegistration( popupLabel ) {
  const nextShowKey = _getNextShowKey( popupLabel );

  localStorage.setItem( nextShowKey, _getFutureDate( FOREVER ) );
}

/**
 * Checks today's date against that in local storage for the purposes of
 * displaying a popup.
 * @param {string} popupLabel - label for this popup.
 * @returns {boolean} True if the popup should display, false otherwise.
 */
function showEmailPopup( popupLabel ) {
  const nextShowKey = _getNextShowKey( popupLabel );

  const today = new Date().getTime();
  const nextDisplayDate = Number( localStorage.getItem( nextShowKey ) ) || 0;
  return today > nextDisplayDate;
}

function throttle( func, wait, options ) {
  let context;
  let args;
  let result;
  let timeout = null;
  let previous = 0;
  if ( !options ) options = {};

  function later() {
    previous = options.leading === !1 ? 0 : Date.now();
    timeout = null;
    result = func.apply( context, args );
    if ( !timeout ) context = args = null;
  }
  return function() {
    const now = Date.now();
    if ( !previous && options.leading === !1 ) previous = now;
    const remaining = wait - ( now - previous );
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
  let UNDEFINED;
  const defaults = {
    scrollPercent: 50,
    throttleDelay: 10,
    targetElement: null,
    cb: function() {
      return UNDEFINED;
    }
  };

  opts = _assign( defaults, opts || {} );

  function _getScrollTargetPosition() {
    const elHeight = elToShow.offsetHeight;
    if ( opts.targetElement && opts.targetElement.length ) {
      const top = opts.targetElement.offset().top;
      return top + elHeight;
    }
    const percentageTarget = document.body.offsetHeight * ( opts.scrollPercent / 100 );
    return percentageTarget + elHeight;

  }

  function _scrollTargetPositionReached() {
    const windowHeight = window.innerHeight;
    const windowTop = window.pageYOffset;
    const windowBottom = windowTop + windowHeight;
    const scrollTargetPosition = _getScrollTargetPosition();
    return windowBottom > scrollTargetPosition;
  }

  const handler = throttle( function( event ) {
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
  showOnScroll: showOnScroll,
  throttle: throttle
};
