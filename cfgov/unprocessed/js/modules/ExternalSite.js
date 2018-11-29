/* ==========================================================================
   External Site Initialization
   Used on at least `/external-site/`.
   ========================================================================== */

import { checkDom } from '../modules/util/atomic-helpers';

/**
 * ExternalSite
 * @class
 *
 * @classdesc Initializes a new ExternalSite instance.
 *
 * @param {HTMLElement} element DOM Element.
 */
function ExternalSite( element ) {
  const BASE_CLASS = 'external-site_container';
  const TOTAL_DURATION = 5;
  const INTERVAL = 1000;

  const _dom = checkDom( element, BASE_CLASS );
  const _durationEl = _dom.querySelector( '.external-site_reload-container' );
  const _directEl = _dom.querySelector( '.external-site_proceed-btn' );
  let _duration = TOTAL_DURATION;
  let _intervalId;

  /**
   * Initialize the events and timer.
   */
  function init() {
    _intervalId = setInterval( _tick, INTERVAL );
    _directEl.addEventListener( 'click', _proceedClicked );
  }

  /**
   * Timer tick. Update the content and go to the URL if timer is zero.
   */
  function _tick() {
    _updateContent();
    if ( --_duration === 0 ) {
      _gotoUrl();
    }
  }

  /**
   * Go to the redirect URL.
   */
  function _gotoUrl() {
    const _formEl = _dom.querySelector( 'form#proceed' );
    clearInterval( _intervalId );
    _formEl.submit();
  }

  /**
   * Update the timer HTML content.
   */
  function _updateContent() {
    const plurality = _duration === 1 ? '' : 's';
    const content = '<span class=\'external-site_reload-duration\'>' +
                  _duration + '</span> second' + plurality;
    _durationEl.innerHTML = content;
  }

  /**
   * Proceed to external site button was clicked.
   * @param {Object} event Click event object.
   */
  function _proceedClicked( event ) {
    event.stopImmediatePropagation();
    _gotoUrl();
  }

  this.init = init;

  return this;
}

// Expose public methods.
export default ExternalSite;
