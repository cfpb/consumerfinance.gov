/* ==========================================================================
   Bureau structure.
   Scripts for `/the-bureau/bureau-structure/`.

   TODO: Remove jQuery, burn slick.js, and refactor ContentSlider.js.
   ========================================================================== */

'use strict';

var $ = require( 'jquery' );
require( 'slick' );

var ContentSlider = require( '../../../../modules/ContentSlider' );
var BreakpointHandler = require( '../../../../modules/BreakpointHandler' );
var Expandable = require( '../../../../molecules/Expandable' );

var _slider;

function init() {

  var bpSettings = {
    breakpoint: 600,
    type:       'max',
    enter:      _createSlider,
    leave:      _destroySlider
  };

  new BreakpointHandler( bpSettings ); // eslint-disable-line no-new, no-inline-comments, max-len
}

function initExpandables() {
  // Initialize the Expandable.
  var selector = '.m-expandable';
  var expandables = document.querySelectorAll( selector );
  var expandable;
  for ( var i = 0, len = expandables.length; i < len; i++ ) {
    expandable = new Expandable( expandables[i] );
    expandable.init();
  }
}

function _createSlider() {
  var $legend = $( '.org-chart_legend' ).parent().clone();
  var $contentSlider = $( '#content-slider' );
  // Hide org chart branches.
  $( '.org-chart_branches' ).hide();
  // Show content slider & mobile nav links.
  $( '#content-slider, .content-hide' ).show();
  // Initialize slider.
  _slider = new ContentSlider( $contentSlider, 1 );

  // Overwrite the default method to set height
  // There are performance implications of doing so
  // as noted here https://github.com/kenwheeler/slick/issues/83.
  // ( Although wildly exaggerated. )
  _slider.slickObj.setHeight = function setHeight() {
      this.$list.css( 'height', 'auto' );
  };

  _slider.slickObj.options.onAfterChange =
    function onAfterChange( slider, currInd, targetInd ) {
      // Add legend to the nodes list if doesn't exist.
      var add_legend = currInd > 0 &&
                       $( '.slick-active .org-chart_legend' ).length === 0;
      if ( add_legend ) {
        $( '.slick-active > .org-chart_nodes' ).append( $legend );
      }
      $contentSlider.height( 'auto' );
      // Init the Expandable after the nodes have been cloned.
      initExpandables();
    };
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

init();
