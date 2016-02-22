'use strict';

// Required modules.
var atomicCheckers = require( '../modules/util/atomic-checkers' );
var Expandable = require( '../molecules/Expandable' );

/**
 * SecondaryNavigation
 * @class
 *
 * @classdesc Initializes a new Filterable-List-Controls organism.
 *
 * @param {HTMLNode} element
 *   The DOM element within which to search for the organism.
 */
function SecondaryNavigation( element ) {
  var BASE_CLASS = 'o-secondary-navigation';

  var _dom = atomicCheckers.validateDomElement(
    element, BASE_CLASS, 'SecondaryNavigation' );

  /**
   * Initialize FilterableListControls instance.
  */
  function init() {
    var expandable = new Expandable( _dom );
    expandable.init();
  }

  this.init = init;
  return this;
}

module.exports = SecondaryNavigation;
