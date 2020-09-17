import { assign } from './assign';
import throttle from 'lodash.throttle';
import webStorageProxy from './web-storage-proxy';

// If cookies are turned off, we set localStorage variables to an empty object.
let _localStorage;

try {
  _localStorage = window.localStorage;
} catch ( err ) {
  _localStorage = null;
}

/**
 * Stores/retrieves email signup data in localStorage.
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
  return date.setTime( date.getTime() + days * 24 * 60 * 60 * 1000 );
}

/**
 * Record in local storage that the email popup has been viewed.
 * @param {string} popupLabel - label for this popup.
 */
function recordEmailPopupView( popupLabel ) {
  const countKey = _getCountKey( popupLabel );
  const nextShowKey = _getNextShowKey( popupLabel );

  let count = Number( webStorageProxy.getItem( countKey, _localStorage ) ) || 0;
  const max = POPUP_WAIT_PERIOD.length - 1;
  count = count >= max ? max : count;
  const days = POPUP_WAIT_PERIOD[count];
  webStorageProxy.setItem( countKey, count + 1, _localStorage );
  webStorageProxy.setItem( nextShowKey, _getFutureDate( days ), _localStorage );
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
  webStorageProxy.setItem( countKey, count, _localStorage );
  webStorageProxy.setItem( nextShowKey, _getFutureDate( days ), _localStorage );
}

/**
 * Sets email popup key in local storage with a very long expiry date.
 * @param {string} popupLabel - label for this popup.
 */
function recordEmailRegistration( popupLabel ) {
  const nextShowKey = _getNextShowKey( popupLabel );

  webStorageProxy.setItem(
    nextShowKey,
    _getFutureDate( FOREVER ),
    _localStorage
  );
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
  const nextDisplayDate = Number(
    webStorageProxy.getItem( nextShowKey, _localStorage )
  ) || 0;
  return today > nextDisplayDate;
}

/**
 * Show the popup when scrolling.
 * @param  {HTMLNode} elToShow - Element to check the height of.
 * @param  {Object} opts - Object with callback and target HTML element.
 */
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

  opts = assign( defaults, opts || {} );

  /**
   * @returns {number} Scroll target vertical position in pixels from top.
   */
  function _getScrollTargetPosition() {
    const elHeight = elToShow.offsetHeight;
    if ( opts.targetElement && opts.targetElement.length ) {
      const top = opts.targetElement.offset().top;
      return top + elHeight;
    }
    const percentageTarget = document.body.offsetHeight *
                             ( opts.scrollPercent / 100 );
    return percentageTarget + elHeight;
  }

  /**
   * @returns {boolean}
   *   True if the scroll position has been reached, false otherwise.
   */
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

export {
  showEmailPopup,
  recordEmailPopupView,
  recordEmailRegistration,
  recordEmailPopupClosure,
  showOnScroll
};
