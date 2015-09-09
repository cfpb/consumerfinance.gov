/* ==========================================================================
   Get Breakpoint State
   ========================================================================== */

'use strict';

var _breakpointsConfig = require( '../../config/breakpoints-config' );
var _getViewportDimensions = require( './get-viewport-dimensions' )
                             .getViewportDimensions;

function _inBreakpointRange( breakpointRange, width ) {
  var min = breakpointRange.min || 0;
  var max = breakpointRange.max || Number.POSITIVE_INFINITY;

  return min <= width && width <= max;
}

/**
 * @returns {object} An object literal with Boolean
 * isMobile, isTablet, isDesktop, isWall, isSmall properties.
 * @param {integer} width Current window width.
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

// Expose public methods.
module.exports = { get: get };
