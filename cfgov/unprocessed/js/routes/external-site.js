/* ==========================================================================
   Scripts for `/external-site/`.
   ========================================================================== */

import { checkDom } from '@cfpb/cfpb-atomic-component/src/utilities/atomic-helpers.js';

const BASE_CLASS = 'external-site';
const TOTAL_DURATION = 5;
const INTERVAL = 1000;

/**
 * ExternalSite
 * @class
 *
 * @classdesc Initializes a new ExternalSite instance.
 *
 * @param {HTMLElement} element DOM Element.
 */
function ExternalSite( element ) {
  const _dom = checkDom( element, BASE_CLASS );
  const _durationEl = _dom.querySelector( `.${ BASE_CLASS }_reload-container` );
  const _proceedBtnEl = _dom.querySelector( `#${ BASE_CLASS }_proceed-btn` );
  let _duration = TOTAL_DURATION;
  let _intervalId;

  /**
   * Initialize the events and timer.
   */
  function init() {
    _intervalId = setInterval( _tick, INTERVAL );
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
    clearInterval( _intervalId );
    document.location = _proceedBtnEl.href;
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

  this.init = init;

  return this;
}

const externalSiteDom = document.querySelector( `.${ BASE_CLASS }` );

if ( externalSiteDom ) {
  const externalSite = new ExternalSite( externalSiteDom );
  externalSite.init();
}

export default ExternalSite;
