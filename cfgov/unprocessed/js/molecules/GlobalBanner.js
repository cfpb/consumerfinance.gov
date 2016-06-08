/* ==========================================================================
   Collapsing Global banner.
   Remember banner state (collapsed or open) across sessions.
   ========================================================================== */

'use strict';

// Required modules.
var atomicHelpers = require( '../modules/util/atomic-helpers' );
var Expandable = require( '../organisms/Expandable' );
var webStorageProxy = require( '../modules/util/web-storage-proxy' );
var standardType = require( '../modules/util/standard-type' );

/**
 * GlobalBanner
 * @class
 *
 * @classdesc Initializes a new GlobalBanner molecule.
 *
 * @param {HTMLNode} element
 *   The DOM element within which to search for the molecule.
 * @returns {GlobalBanner} An instance.
 */
function GlobalBanner( element ) {

  var BASE_CLASS = 'm-global-banner';
  var EXPANDED_STATE = 'globalBannerIsExpanded';

  var _dom = atomicHelpers.checkDom( element, BASE_CLASS );
  var _expandable;

  /**
   * Set up DOM references and event handlers.
   * @returns {GlobalBanner|undefined} An instance,
   *   or undefined if it was already initialized.
   */
  function init() {
    if ( !atomicHelpers.setInitFlag( _dom ) ) {
      return standardType.UNDEFINED;
    }

    // Init Expandable.
    var isExpanded = webStorageProxy.getItem( EXPANDED_STATE ) !== 'false';
    _expandable = new Expandable( _dom.querySelector( '.o-expandable' ) );
    _expandable.init( isExpanded && _expandable.EXPANDED );

    _initEvents();

    return this;
  }

  /**
   * Run when the beta in-progress banner has been clicked.
   */
  function _initEvents() {
    _expandable.addEventListener( 'click', toggleStoredState );
  }

  /**
   * Remove event handlers and local storage data.
   */
  function destroy() {
    _expandable.removeEventListener( 'click', toggleStoredState );
    webStorageProxy.removeItem( EXPANDED_STATE, true );
  }

  /**
   * Toggle the boolean value stored in a web storage.
   * @returns {boolean} Returns value stored in the web storage,
   * either true or false.
   */
  function toggleStoredState() {
    var value = webStorageProxy.getItem( EXPANDED_STATE );

    if ( value === 'false' ) {
      webStorageProxy.setItem( EXPANDED_STATE, true );
    } else {
      webStorageProxy.setItem( EXPANDED_STATE, false );
    }
    return value;
  }

  this.init = init;
  this.destroy = destroy;
  this.toggleStoredState = toggleStoredState;

  return this;
}

// Expose public methods.
module.exports = GlobalBanner;
