/* ==========================================================================
   Footer Button: Scroll to Top
   ========================================================================== */

'use strict';

var $ = require( 'jquery' );

var ANIMATION_DURATION = 300;

/**
 * Set up event handler for button to scroll to top of page.
 * Add event listeners and disable Google Tag Manager tracking
 * for a link click.
 */
function init() {
  var footerBtnDom = document.querySelector( '.js-return-to-top' );
  footerBtnDom.addEventListener( 'click', _handleFooterBtnClick );

  // Disable Google Tag Manager tracking on this link.
  footerBtnDom.setAttribute( 'data-gtm_ignore', 'true' );
}

function _handleFooterBtnClick( event ) {
  event.preventDefault();

  // TODO: Investigate using a CSS transition in place of jquery.
  $( 'html, body' ).animate( { scrollTop: 0 }, ANIMATION_DURATION );
}

module.exports = { init: init };
