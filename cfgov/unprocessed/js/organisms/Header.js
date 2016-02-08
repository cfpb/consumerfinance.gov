'use strict';

// Required modules.
var atomicCheckers = require( '../modules/util/atomic-checkers' );
var GlobalSearch = require( '../molecules/GlobalSearch.js' );

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

  /**
   * @returns {Object} The Header instance.
   */
  function init() {
    _globalSearch = new GlobalSearch( _dom );
    _globalSearch.init();

    return this;
  }

  this.init = init;

  return this;
}

module.exports = Header;
