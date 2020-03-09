/* ==========================================================================
   Get Breakpoint State
   ========================================================================== */

import varsBreakpoints from '@cfpb/cfpb-core/src/vars-breakpoints';

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
 *   bpXS, bpSM, bpMED, bpLG, bpXL properties.
 */
function getBreakpoint( width ) {
  const breakpointState = {};
  width = width || window.innerWidth;

  let rangeKey;
  // eslint-disable-next-line guard-for-in
  for ( rangeKey in varsBreakpoints ) {
    breakpointState[rangeKey] = _inBreakpointRange(
      varsBreakpoints[rangeKey],
      width
    );
  }

  return breakpointState;
}

// Constants for breakpoint groupings.
const MOBILE = 'mobile';
const TABLET = 'tablet';
const DESKTOP = 'desktop';

/**
 * Checks whether the current breakpoint is in a particular breakpoint group.
 * @param {string} breakpointGroup - Breakpoint group names.
 * @returns {boolean} True if in the breakpoint group, otherwise false.
 */
function viewportIsIn( breakpointGroup ) {
  let response = false;
  const currentBreakpoint = getBreakpoint();

  if (
    ( breakpointGroup === MOBILE && currentBreakpoint.bpXS ) ||
    ( breakpointGroup === TABLET && currentBreakpoint.bpSM ) ||
    ( breakpointGroup === DESKTOP &&
      ( currentBreakpoint.bpMED ||
        currentBreakpoint.bpLG ||
        currentBreakpoint.bpXL
      )
    )
  ) {
    response = true;
  }

  return response;
}

// Expose public methods.
export {
  MOBILE,
  TABLET,
  DESKTOP,
  getBreakpoint,
  viewportIsIn
};
