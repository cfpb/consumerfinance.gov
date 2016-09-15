/* ==========================================================================
   Footer Button: Scroll to Top

   Code copied from the following with minimal modifications :

   - http://stackoverflow.com/questions/21474678/
     scrolltop-animation-without-jquery
   ========================================================================== */

'use strict';

// Required modules.
var behavior = require( './util/behavior' );

/**
 * Set up event handler for button to scroll to top of page.
 */
function init() {
  if ( 'requestAnimationFrame' in window === false ) {
    return;
  }

  behavior.attach( 'return-to-top', 'click', function( event ) {
    event.preventDefault();
    _scrollToTop();
  } );
}

/**
 *  Duration of the scroll to top of the page.
 */
function _scrollToTop() {
  var SCROLL_DURATION = 300;
  var SCROLL_STEP_DURATION = 10;
  var scrollHeight = window.scrollY;
  var scrollStep = Math.PI / ( SCROLL_DURATION / SCROLL_STEP_DURATION );
  var cosParameter = scrollHeight / 2;
  var scrollCount = 0;
  var scrollMargin;

  window.requestAnimationFrame( _step );

  /**
   * Decrement scroll Y position.
   */
  function _step() {
    window.setTimeout( function() {
      if ( window.scrollY !== 0 ) {
        window.requestAnimationFrame( _step );
        scrollCount += 1;
        scrollMargin = cosParameter - cosParameter *
                       Math.cos( scrollCount * scrollStep );
        window.scrollTo( 0, scrollHeight - scrollMargin );
      }
    }, SCROLL_STEP_DURATION );
  }
}

module.exports = { init: init };
