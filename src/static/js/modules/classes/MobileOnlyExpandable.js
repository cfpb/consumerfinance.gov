'use strict';

var $ = require( 'jquery' );
var jQuery = $;
var BreakpointHandler = require( './BreakpointHandler' );

/**
 * MobileOnlyExpandable
 * @class
 *
 * @classdesc Hides content in an expandable for mobile screens.
 * When viewport size drops below specified max-width breakpoint,
 * visible expandable content is hidden.
 * When breakpoint is exceeded, expandable content is shown.
 * (Expandable trigger is currently hidden/shown via media query.)
 *
 * @param {object} elem jQuery `expandable` element.
 * @param {number} breakpoint Mobile max-width value.
 */
function MobileOnlyExpandable( elem, breakpoint ) {
  this.expandable = elem;
  this.expandableTarget = this.expandable.children( '.expandable_target' );
  this.breakpoint = breakpoint;

  // Make sure we have necessary elements before proceeding.
  if ( this.expandable instanceof jQuery &&
       this.expandableTarget instanceof jQuery ) {
    this.breakpointHandler = new BreakpointHandler( {
      breakpoint: this.breakpoint,
      type:       'max',
      enter:      $.proxy( this.closeExpandable, this ),
      leave:      $.proxy( this.openExpandable, this )
    } );
  }
}

function closeExpandable() {
  // Click to close expandable if it is open.
  // TODO: alternative to click event.
  var isExpanded = this.expandable.hasClass( 'expandable__expanded' );
  if ( isExpanded ) {
    this.expandableTarget.click();
  }
}

function openExpandable() {
  // Click to open expandable if it is closed.
  // TODO: alternative to click event.
  var isExpanded = this.expandable.hasClass( 'expandable__expanded' );
  if ( !isExpanded ) {
    this.expandableTarget.click();
  }
}

// Expose public methods.
MobileOnlyExpandable.prototype.closeExpandable = closeExpandable;
MobileOnlyExpandable.prototype.openExpandable = openExpandable;
module.exports = MobileOnlyExpandable;
