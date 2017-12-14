// Required modules.
const atomicHelpers = require( '../modules/util/atomic-helpers' );
const Expandable = require( '../organisms/Expandable' );
const standardType = require( '../modules/util/standard-type' );

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
  const BASE_CLASS = 'o-secondary-navigation';

  const _dom = atomicHelpers.checkDom( element, BASE_CLASS );

  /**
   * @returns {SecondaryNavigation|undefined} An instance,
   *   or undefined if it was already initialized.
   */
  function init() {
    if ( !atomicHelpers.setInitFlag( _dom ) ) {
      return standardType.UNDEFINED;
    }

    const expandable = new Expandable( _dom );
    expandable.init();

    return this;
  }

  this.init = init;
  return this;
}

module.exports = SecondaryNavigation;
