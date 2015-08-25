'use strict';

var $ = require( 'jquery' );
var getBreakpointState = require( '../util/breakpoint-state' ).get;
var _breakpointsConfig = require( '../../config/breakpoints-config' );

// Used for checking browser capabilities.
// TODO: Check what browsers this is necessary for and
// check whether it is still applicable.
var _viewportEl;
var _propPrefix;

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
  if ( !opts ||
       !opts.breakpoint ||
       !opts.enter ||
       !opts.leave ) {
    throw new Error( 'BreakpointHandler constructor requires arguments!' );
  }

  var breakpoint = opts.breakpoint;
  var type = opts.type || 'max';

  this.match = false;
  this.type = type;
  this.breakpoint = _breakpointsConfig[breakpoint] &&
                    _breakpointsConfig[breakpoint][type] ||
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
  // TODO: Check what browsers this is necessary for and
  // check whether it is still applicable.
  _viewportEl = window;
  _propPrefix = 'inner';
  var modernBrowser = 'innerWidth' in window;
  if ( !modernBrowser ) {
    _viewportEl = document.documentElement || document.body;
    _propPrefix = 'client';
  }

  self.handleViewportChange();
  self.watchWindowResize();
}

function watchWindowResize() {
  var self = this;
  $( window ).bind( 'resize', function() {
    self.handleViewportChange();
  } );
}

function handleViewportChange() {
  var width = _viewportEl[_propPrefix + 'Width'];
  var match = this.testBreakpoint( width );
  var breakpointState;

  if ( match !== this.match ) {
    breakpointState = getBreakpointState( width );
    if ( match && this.enter ) this.enter( breakpointState );
    else if ( this.leave ) this.leave( breakpointState );
  }

  this.match = match;
}

function testBreakpoint( width ) {
  var bp = {
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
BreakpointHandler.getBreakpointState = getBreakpointState;

module.exports = BreakpointHandler;
