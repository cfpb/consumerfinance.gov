/* ==========================================================================
   Bureau structure.
   Scripts for `/the-bureau/bureau-structure/`.
   ========================================================================== */

'use strict';

require( 'slick' );

var ContentSlider = require( '../../../modules/content-slider' ).contentSlider;
var BreakpointHandler = require( '../../../modules/breakpoint-handler' ).BreakpointHandler;

$('document').ready(function () {
  var slider, handler;
  if (!$( 'html' ).hasClass( 'lt-ie9' )) {
    handler = new BreakpointHandler( {
      breakpoint: 599,
      type:       'max',
      enter:      function() {
        // close any open expandables
        $( '.org-chart' ).find( '.expandable__expanded .expandable_target' ).click();
        // hide org chart branches
        $( '.org-chart_branches' ).hide();
        // show content slider & mobile nav links
        $( '#content-slider, .content-hide' ).show();
        // init slider
        slider = new ContentSlider( '#content-slider', 1);
      },
      leave:      function() {
        // destroy slider
        slider && slider.destroy();
        slider = null;
        // hide content slider & mobile nav links
        $( '#content-slider, .content-hide' ).hide();
        // show org chart branches
        $( '.org-chart_branches' ).show();
      }
    });
  }
});
