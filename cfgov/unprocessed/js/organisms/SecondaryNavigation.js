'use strict';

// Required modules.
var atomicHelpers = require( '../modules/util/atomic-helpers' );
var Expandable = require( '../organisms/Expandable' );
var standardType = require( '../modules/util/standard-type' );

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

  var _dom = atomicHelpers.checkDom( element, BASE_CLASS );

  /**
   * @returns {SecondaryNavigation|undefined} An instance,
   *   or undefined if it was already initialized.
   */
  function init() {
    if ( !atomicHelpers.setInitFlag( _dom ) ) {
      return standardType.UNDEFINED;
    }

    var expandable = new Expandable( _dom );
    expandable.init();

    return this;
  }

  this.init = init;
  return this;
}

module.exports = SecondaryNavigation;
