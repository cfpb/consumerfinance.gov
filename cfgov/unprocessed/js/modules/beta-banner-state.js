/* ==========================================================================
   Collapsing Beta banner.
   Remember banner state (collapsed or open) across sessions.
   ========================================================================== */

'use strict';

// Required modules.
var Expandable = require( '../molecules/Expandable' );
var _storage = require( './util/web-storage-proxy' );

// Private variables.
var _expandable;

// Constants.
var EXPANDED_STATE = 'betaBannerIsExpanded';


/**
 * Set up DOM references and event handlers.
 */
function init() {

  // Init Expandable.
  var betaBannerDom = document.querySelector( '#beta-banner' );
  var isExpanded = _storage.getItem( EXPANDED_STATE ) !== 'false';

  _expandable = new Expandable( betaBannerDom );
  _expandable.init( isExpanded && _expandable.EXPANDED );

  _initEvents();
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
  _storage.removeItem( EXPANDED_STATE, true );
}

/**
 * Toggle the boolean value stored in a web storage.
 * @returns {boolean} Returns value stored in the web storage,
 * either true or false.
 */
function toggleStoredState() {
  var value = _storage.getItem( EXPANDED_STATE );

  if ( value === 'false' ) {
    _storage.setItem( EXPANDED_STATE, true );
  } else {
    _storage.setItem( EXPANDED_STATE, false );
  }
  return value;
}

// Expose public methods.
module.exports = { init:              init,
                   destroy:           destroy,
                   toggleStoredState: toggleStoredState
                 };
