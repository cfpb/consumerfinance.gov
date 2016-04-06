'use strict';

// Required modules.
var atomicHelpers = require( '../modules/util/atomic-helpers' );
var footerButton = require( '../modules/footer-button' );


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

  var _dom = atomicHelpers.checkDom( element, BASE_CLASS, 'Footer' );

  /**
   * @returns {Footer} The instance.
   */
  function init() {
    footerButton.init();

    return this;
  }

  this.init = init;

  return this;
}

module.exports = Footer;
