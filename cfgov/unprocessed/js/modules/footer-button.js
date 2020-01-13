/* ==========================================================================
   Footer Button: Scroll to Top
   Code copied from the following with minimal modifications :
   - https://stackoverflow.com/questions/21474678/
   scrolltop-animation-without-jquery
   ========================================================================== */

// Required modules.
import * as behavior from './util/behavior';

/**
 * Set up event handler for button to scroll to top of page.
 */
function init() {
  behavior.attach( 'return-to-top', 'click', event => {
    event.preventDefault();
    _scrollToTop();
  } );
}

/**
 *  Duration of the scroll to top of the page.
 */
function _scrollToTop() {
  const SCROLL_DURATION = 300;
  const SCROLL_STEP_DURATION = 10;
  const scrollHeight = window.scrollY;
  const scrollStep = Math.PI / ( SCROLL_DURATION / SCROLL_STEP_DURATION );
  const cosParameter = scrollHeight / 2;
  let scrollCount = 0;
  let scrollMargin;

  // If requestAnimationFrame is not supported, return to top immediately.
  if ( 'requestAnimationFrame' in window === false ) {
    window.scrollTo( 0, 0 );
    _setFocus();
    return;
  }

  window.requestAnimationFrame( _step );

  /**
   * Decrement scroll Y position.
   */
  function _step() {
    if ( window.scrollY === 0 ) {
      _setFocus();
    } else {
      window.setTimeout( () => {
        scrollCount += 1;
        const adjustVal = cosParameter * Math.cos( scrollCount * scrollStep );
        scrollMargin = cosParameter - adjustVal;
        window.scrollTo( 0, scrollHeight - scrollMargin );
        window.requestAnimationFrame( _step );
      }, SCROLL_STEP_DURATION );
    }
  }
}

/**
 *  Move focus to the top of the page.
 */
function _setFocus() {
  document.documentElement.tabIndex = 0;
  document.documentElement.focus();
}

export { init };
