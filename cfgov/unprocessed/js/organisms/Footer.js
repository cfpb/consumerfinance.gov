'use strict';

// Required modules.
var atomicHelpers = require( '../modules/util/atomic-helpers' );
var footerButton = require( '../modules/footer-button' );
var standardType = require( '../modules/util/standard-type' );

/**
 * Footer
 * @class
 *
 * @classdesc Initializes the organism.
 *
 * @param {HTMLNode} element
 *   The DOM element within which to search for the organism.
 * @returns {Footer} An instance.
 */
function Footer( element ) {

  var BASE_CLASS = 'o-footer';

  var _dom = atomicHelpers.checkDom( element, BASE_CLASS );

  /**
   * @returns {Footer|undefined} An instance,
   *   or undefined if it was already initialized.
   */
  function init() {
    if ( !atomicHelpers.setInitFlag( _dom ) ) {
      return standardType.UNDEFINED;
    }

    footerButton.init();

    return this;
  }

  this.init = init;

  return this;
}

module.exports = Footer;
