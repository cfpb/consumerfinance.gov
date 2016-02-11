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

  /**
   * @returns {Object} The Header instance.
   */
  function init() {
    _globalSearch = new GlobalSearch( _dom );
    _globalSearch.addEventListener( 'toggle', _searchClicked );
    _globalSearch.init();

    _megaMenu = new MegaMenu( _dom );
    _megaMenu.addEventListener( 'triggerClick', _megaMenuClicked );
    _megaMenu.init();

    return this;
  }

  /**
   * Handler for opening the search.
   */
  function _searchClicked() {
    _megaMenu.collapse();
  }

  /**
   * Handler for opening the mega menu.
   */
  function _megaMenuClicked() {
    _globalSearch.collapse();
  }

  this.init = init;

  return this;
}

module.exports = Header;
