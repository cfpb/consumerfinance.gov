/* ==========================================================================
   Get Breakpoint State
   ========================================================================== */

const _breakpointsConfig = require( '../../config/breakpoints-config' );
const _getViewportDimensions = require( './get-viewport-dimensions' )
  .getViewportDimensions;

/**
 * @param {Object} breakpointRange - Object containing breakpoint constants.
 * @param {integer} width - Current window width.
 * @returns {boolean} Whether the passed width is within a breakpoint range.
 */
function _inBreakpointRange( breakpointRange, width ) {
  const min = breakpointRange.min || 0;
  const max = breakpointRange.max || Number.POSITIVE_INFINITY;

  return min <= width && width <= max;
}

/**
 * @param {integer} width - Current window width.
 * @returns {Object} An object literal with boolean
 *   isBpXS, isBpSM, isBpMED, isBpLG, isBpXL properties.
 */
function get( width ) {
  const breakpointState = {};
  let breakpointKey;
  width = width || _getViewportDimensions().width;

  // eslint-disable-next-line guard-for-in
  for ( const rangeKey in _breakpointsConfig ) {
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
  let response = false;
  const currentBreakpoint = get();
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
