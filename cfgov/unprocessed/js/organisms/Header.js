'use strict';

// Required modules.
var atomicCheckers = require( '../modules/util/atomic-checkers' );
var GlobalSearch = require( '../molecules/GlobalSearch.js' );
var MegaMenu = require( '../organisms/MegaMenu.js' );

/**
 * Header
 * @class
 *
 * @classdesc Initializes a new Header organism.
 *
 * @param {HTMLNode} element
 *   The DOM element within which to search for the organism.
 * @returns {Object} An Header instance.
 */
function Header( element ) {

  var BASE_CLASS = 'o-header';

  var _dom =
    atomicCheckers.validateDomElement( element, BASE_CLASS, 'Header' );
  var _globalSearch;
  var _megaMenu;
  var _overlay;

  /**
   * @param {HTMLNode} overlay
   *   Overlay to show/hide when mobile mega menu is shown.
   * @returns {Object} The Header instance.
   */
  function init( overlay ) {
    _overlay = overlay;
    _globalSearch = new GlobalSearch( _dom );
    _globalSearch.addEventListener( 'expandBegin', _searchExpandBegin );
    _globalSearch.init();

    _megaMenu = new MegaMenu( _dom );
    _megaMenu.addEventListener( 'rootExpandBegin', _megaMenuExpandBegin );
    _megaMenu.addEventListener( 'rootCollapseEnd', _megaMenuCollapseEnd );
    _megaMenu.init();

    return this;
  }

  /**
   * Handler for opening the search.
   */
  function _searchExpandBegin() {
    _megaMenu.collapse();
  }


  /**
   * Handler for when the mega menu begins expansion.
   * Collapse the global search.
   */
  function _megaMenuExpandBegin() {
    _globalSearch.collapse();
    _overlay.classList.remove( 'u-hidden' );
  }

  /**
   * Handler for when the mega menu ends collapsing.
   * Show an overlay.
   */
  function _megaMenuCollapseEnd() {
    _overlay.classList.add( 'u-hidden' );
  }

  this.init = init;

  return this;
}

module.exports = Header;
