/* ==========================================================================
   Get Breakpoint State
   ========================================================================== */

import varsBreakpoints from '@cfpb/cfpb-core/src/vars-breakpoints';

/**
 * @returns {number} The base font size set on the body element.
 */
function _getBodyBaseFontSize() {
  let fontSize = getComputedStyle( document.body ).fontSize;
  fontSize = fontSize === '' ? -1 : fontSize;
  return parseFloat( fontSize );
}

/**
 * @param {Object} breakpointRange - Object containing breakpoint constants.
 *   For example, for `bpXS` the value `{ min: 0, max: 600 }` would be passed.
 * @param {integer} width - Current window width.
 * @returns {boolean} Whether the passed width is within a breakpoint range.
 */
function _inBreakpointRange( breakpointRange, width ) {
  let breakpointRangeMin = breakpointRange.min;
  let breakpointRangeMax = breakpointRange.max;

  // Whether the user has set a custom size for the font in their browser.
  const useEmsConversation = _getBodyBaseFontSize() > 0 &&
                             _getBodyBaseFontSize() !== 16;
  if ( useEmsConversation ) {
    /* 16 = base font size without adjustments.
       The CSS converts breakpoints to ems, which then change the width of the
       pixel width of the breakpoint. In JavaScript, the breakpoints are defined
       in pixels, so we first convert them to ems using the 16px base font size
       and then multiply them by any adjustments set by customizations of the
       font size in the user's browser. */
    breakpointRangeMin = ( breakpointRangeMin / 16 ) * _getBodyBaseFontSize();
    breakpointRangeMax = ( breakpointRangeMax / 16 ) * _getBodyBaseFontSize();
  }

  const min = breakpointRangeMin || 0;
  const max = breakpointRangeMax || Number.POSITIVE_INFINITY;

  return min <= width && width <= max;
}

/**
 * @param {integer} width - Current window width.
 * @returns {Object} An object literal with boolean
 *   bpXS, bpSM, bpMED, bpLG, bpXL properties.
 */
function getBreakpointState( width ) {
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
  const currentBreakpoint = getBreakpointState();

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
  getBreakpointState,
  viewportIsIn
};
