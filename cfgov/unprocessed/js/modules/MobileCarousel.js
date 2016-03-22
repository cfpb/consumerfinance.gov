/* ==========================================================================
   Creates a mobile Slick carousel.
   ========================================================================== */

'use strict';

var $ = require( 'jquery' );
require( 'slick' );
var BreakpointHandler = require( './BreakpointHandler' );
var breakpointsConfig = require( '../config/breakpoints-config' );

/**
* MobileCarousel
* @class
* @param {number} breakpointPx
*   The pixel breakpoint to enable the mobile carousel at.
*/
function MobileCarousel( breakpointPx ) {
  // Initialization can happen here, like an `init` method.
  var _breakpointPx = breakpointPx || breakpointsConfig.bpXS.max;
  var _targetDom;

  /**
  * Handling entering of a breakpoint by enabling the Slick carousel.
  */
  function _enterBreakpoint() {
    _targetDom.slick( { dots: true } );
  }

  /**
  * Handling leaving of a breakpoint by disabling the Slick carousel.
  */
  function _leaveBreakpoint() {
    _targetDom.unslick();
  }

  /**
  * @param {string} selector A selector for a page DOM element.
  * @returns {Object} A reference to the instance.
  * @throws {Error} If selector is not found.
  */
  function enableOn( selector ) {
    _targetDom = $( selector );
    if ( !selector || !_targetDom ) {
      throw new Error( 'MobileCarousel.enableOn requires a valid selector!' );
    }

    var bpOptions = {
      breakpoint: _breakpointPx,
      type:       'max',
      enter:      _enterBreakpoint,
      leave:      _leaveBreakpoint
    };
    new BreakpointHandler( bpOptions ); // eslint-disable-line no-new

    return this;
  }

  MobileCarousel.prototype.enableOn = enableOn;
  return this;
}

// Export only the class constructor for the file.
module.exports = MobileCarousel;
