import _breakpointsConfig from '../config/breakpoints-config';
import { get as getBreakpointState } from './util/breakpoint-state';

/**
 * BreakpointHandler
 * @class
 * @classdesc On window resize, checks viewport
 * width against a specified breakpoint value or range,
 * and calls `enter` or `leave` callback if breakpoint
 * region has just been entered or exited.
 *
 * @param {object} opts Options object. Takes form:
 * {
 *  breakpoint: number (600) or range [600, 1023],
 *  type:       range, max, or min (type of media query to emulate),
 *  enter:      callback when breakpoint region entered,
 *  leave:      callback when breakpoint region exited
 * }
 */
function BreakpointHandler( opts ) {
  const hasRequiredArgs = Boolean(
    opts && opts.breakpoint && opts.enter && opts.leave
  );

  if ( hasRequiredArgs === false ) {
    throw new Error( 'BreakpointHandler constructor requires arguments!' );
  }

  const breakpoint = opts.breakpoint;
  this.match = false;
  this.type = opts.type || 'max';
  this.breakpoint = _breakpointsConfig[breakpoint] &&
                    _breakpointsConfig[breakpoint][this.type] ||
                    breakpoint;
  this.enter = opts.enter;
  this.leave = opts.leave;

  _init( this );
}

/**
 * Private helper method for instance initialization.
 * @param {object} self Reference to instance.
 */
function _init( self ) {
  self.handleViewportChange();
  self.watchWindowResize();
}

/**
 * Add event listener for changes in the viewport size.
 */
function watchWindowResize() {
  const self = this;
  window.addEventListener( 'resize', function() {
    self.handleViewportChange();
  } );
}

/**
 * Test the viewport size and set whether the test passes on the instance.
 */
function handleViewportChange() {
  const width = window.innerWidth;
  const match = this.testBreakpoint( width );
  let breakpointState;

  if ( match !== this.match ) {
    breakpointState = getBreakpointState( width );
    if ( match && this.enter ) this.enter( breakpointState );
    else if ( this.leave ) this.leave( breakpointState );
  }

  this.match = match;
}

/**
 * @param {number} width The viewport width to test.
 * @returns {boolean}
 *   Whether viewport width is within the expected breakpoint.
 */
function testBreakpoint( width ) {
  const bp = {
    max:   width <= this.breakpoint,
    min:   width >= this.breakpoint,
    range: width >= this.breakpoint[0] && width <= this.breakpoint[1]
  };
  return bp[this.type];
}

// Expose public methods.
BreakpointHandler.prototype.watchWindowResize = watchWindowResize;
BreakpointHandler.prototype.handleViewportChange = handleViewportChange;
BreakpointHandler.prototype.testBreakpoint = testBreakpoint;

export default BreakpointHandler;
