/* ==========================================================================
   Get Breakpoint State
   ========================================================================== */

'use strict';

var _breakpointsConfig = require( '../../config/breakpoints-config' );
var _getViewportDimensions = require( './get-viewport-dimensions' )
                             .getViewportDimensions;

/**
 * @param {Object} breakpointRange - Object containing breakpoint constants.
 * @param {integer} width - Current window width.
 * @returns {boolean} Whether the passed width is within a breakpoint range.
 */
function _inBreakpointRange( breakpointRange, width ) {
  var min = breakpointRange.min || 0;
  var max = breakpointRange.max || Number.POSITIVE_INFINITY;

  return min <= width && width <= max;
}

/**
 * @param {integer} width - Current window width.
 * @returns {Object} An object literal with boolean
 *   isBpXS, isBpSM, isBpMED, isBpLG, isBpXL properties.
 */
function get( width ) {
  var breakpointState = {};
  var breakpointKey;
  width = width || _getViewportDimensions().width;

  for ( var rangeKey in _breakpointsConfig ) { // eslint-disable-line guard-for-in, no-inline-comments, max-len
    breakpointKey = 'is' + rangeKey.charAt( 0 ).toUpperCase() +
                    rangeKey.slice( 1 );
    breakpointState[breakpointKey] =
      _inBreakpointRange( _breakpointsConfig[rangeKey], width );
  }

  return breakpointState;
}

/**
 * Whether currently in the desktop view.
 * @returns {boolean} True if in the desktop view, otherwise false.
 */
function isInDesktop() {
  var response = false;
  var currentBreakpoint = get();
  if ( currentBreakpoint.isBpMED ||
       currentBreakpoint.isBpLG ||
       currentBreakpoint.isBpXL ) {
    response = true;
  }
  return response;
}

// Expose public methods.
module.exports = {
  get: get,
  isInDesktop: isInDesktop
};
