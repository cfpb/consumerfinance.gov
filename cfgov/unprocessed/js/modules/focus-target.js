/* ==========================================================================
   Focus Target

   This is necessary because of a webkit quirk with handling keyboard
   focus with anchor links. It'll mostly be used on the skip nav link.

   If that webkit bug is fixed, remove this JS.

========================================================================== */

'use strict';

var attachBehavior = require( './util/behavior' ).attach;

/**
 * Parse links to handle webkit bug with keyboard focus.
 */
function init() {

  attachBehavior( 'a[href^="#"]', 'click', function behavior() {
    var anchorSelector = this.getAttribute( 'href' );
    var anchorElement = document.querySelector( anchorSelector );
    if ( anchorElement ) {
      anchorElement.setAttribute( 'tabindex', -1 );
      anchorElement.focus();
    }
  } );
}

module.exports = { init: init };
