/* ==========================================================================
   External Site Initialization
   Used on at least `/external-site/`.
   ========================================================================== */

'use strict';

var atomicCheckers = require( '../modules/util/atomic-checkers' );

/**
 * ExternalSite
 * @class
 *
 * @classdesc Initializes a new ExternalSite instance.
 *
 * @param {HTMLElement} element DOM Element.
 */
function ExternalSite( element ) {

  var BASE_CLASS = 'external-site_container';
  var TOTAL_DURATION = 5;
  var INTERVAL = 1000;

  var _dom =
    atomicCheckers.validateDomElement( element, BASE_CLASS, 'ExternalSite' );
  var _durationEl = _dom.querySelector( '.external-site_reload-container' );
  var _directEl = _dom.querySelector( '.external-site_proceed-btn' );
  var _duration = TOTAL_DURATION;
  var _intervalId;

  /**
   * Initialize the events and timer.
   */
  function init() {
    _directEl.addEventListener( 'click', _proceedClicked );
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
    window.location = _durationEl.getAttribute( 'data-url' );
  }

  /**
   * Update the timer HTML content.
   */
  function _updateContent() {
    var plurality = _duration === 1 ? '' : 's';
    var content = '<span class=\'external-site_reload-duration\'>' +
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
module.exports = ExternalSite;
