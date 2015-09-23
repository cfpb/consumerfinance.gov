/* ==========================================================================
   Collapsing Beta banner.
   Remember banner state (collapsed or open) across sessions.
   ========================================================================== */

'use strict';

// Import modules
var $ = require( 'jquery' );
var _storage = require( './util/web-storage-proxy' );

// Private variables.
var _key = 'betaBannerIsCollapsed';

/**
 * Set up DOM references and event handlers.
 */
function init() {

  // DOM references.
  var btnDOM = $( '#beta-banner_btn' );
  var bannerDOM = $( '#beta-banner' );

  // Event handlers.
  btnDOM.click( _betaBannerClicked );

  // Initial state.
  if ( _storage.getItem( _key ) !== 'true' ) {
    bannerDOM.get( 0 ).expand();
  }
}

/**
 * Run when the beta in-progress banner has been clicked.
 * @returns {boolean} always returns false.
 */
function _betaBannerClicked() {
  _toggleStorage();
  return false;
}

/**
 * Toggle the boolean value stored in a web storage.
 * @returns {boolean} Returns value stored in the web storage,
 *   either true or false.
 */
function _toggleStorage() {
  var value = _storage.getItem( _key );
  if ( value === 'false' ) {
    _storage.setItem( _key, true );
  } else {
    _storage.setItem( _key, false );
  }
  return value;
}

// Expose public methods.
module.exports = { init: init };
