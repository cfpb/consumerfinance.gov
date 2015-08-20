/* ==========================================================================
   Collapsing Beta banner.
   Remember banner state (collapsed or open) across sessions.
   ========================================================================== */

'use strict';

// Import modules
var $ = require( 'jquery' );
var _storage = require( './util/web-storage-proxy' );
var ExpandableView = require( './expandable/ExpandableView' );


// Private variables.
var _key = 'betaBannerIsCollapsed';

/**
 * Set up DOM references and event handlers.
 */
function init() {

  // DOM references.
  var btnDOM = $( '#beta-banner_btn' );
  var bannerDOM = $( '#beta-banner' );
  var bannerExpandableView = bannerDOM[0].view;
  bannerExpandableView.on( 'toggle', _toggleStorage );

  // Initial state.
  if ( _storage.getItem( _key ) !== 'true' ) {
    bannerExpandableView.expand();
  }
}

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
