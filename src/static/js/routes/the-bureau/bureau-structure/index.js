/* ==========================================================================
   Bureau structure.
   Scripts for `/the-bureau/bureau-structure/`.
   ========================================================================== */

'use strict';

var $ = require( 'jquery' );
require( 'slick' );

var ContentSlider = require( '../../../modules/content-slider' );
var BreakpointHandler = require( '../../../modules/BreakpointHandler' );

function init() {
  if ( !$( 'html' ).hasClass( 'lt-ie9' ) ) {
    var settings = {
      breakpoint: 599,
      type:       'max',
      enter:      _createSlider,
      leave:      _destroySlider
    };

    var handler = new BreakpointHandler( settings );
  }

  var _slider;
  function _createSlider() {
    // Close any open expandables.
    $( '.org-chart' ).find( '.expandable__expanded .expandable_target' ).click();
    // Hide org chart branches.
    $( '.org-chart_branches' ).hide();
    // Show content slider & mobile nav links.
    $( '#content-slider, .content-hide' ).show();
    // Initialize slider.
    _slider = new ContentSlider( '#content-slider', 1 );
  }

  function _destroySlider() {
    // Destroy slider.
    if ( _slider ) _slider.destroy();
    _slider = null;
    // Hide content slider & mobile nav links.
    $( '#content-slider, .content-hide' ).hide();
    // Show org chart branches.
    $( '.org-chart_branches' ).show();
  }
}

module.exports = { init: init };
