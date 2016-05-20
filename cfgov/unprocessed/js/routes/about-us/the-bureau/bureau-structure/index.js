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
var dataHook = require( '../../../../modules/util/data-hook' );
var standardType = require( '../../../../modules/util/standard-type' );

var _slider;
var $legend;

function init() {

  var bpSettings = {
    breakpoint: 600,
    type:       'max',
    enter:      _createSlider,
    leave:      _destroySlider
  };

  new BreakpointHandler( bpSettings ); // eslint-disable-line no-new, no-inline-comments, max-len
}

var _expandables = [];
function _initExpandables() {
  // Initialize the Expandable.
  var selector = '.m-expandable';
  var expandablesDom = document.querySelectorAll( selector );
  var expandable;
  for ( var i = 0, len = expandablesDom.length; i < len; i++ ) {
    expandable = new Expandable( expandablesDom[i] );
    // Ensure Expandable isn't coming from cloned DOM nodes.
    expandable.destroy();
    expandable.addEventListener( 'expandEnd', _updateHeight );
    expandable.addEventListener( 'collapseEnd', _updateHeight );
    expandable.init();
    _expandables.push( expandable );
  }
}

function _updateHeight() {
  _slider.setHeightToAuto();
}

function _createSlider() {
  $legend = $( '.org-chart_legend' ).parent().clone();
  // Hide org chart branches.
  $( '.org-chart_branches' ).hide();
  // Show content slider & mobile nav links.
  $( '#content-slider, .content-hide' ).show();
  // Initialize slider.
  var sliderElem = document.querySelector( '#content-slider' );
  _slider = new ContentSlider( sliderElem ).init( 1 );
  _slider.addEventListener( 'afterChange', _sliderAfterChangeHandler )
}

function _sliderAfterChangeHandler( event ) {
  var currInd = event.currInd;

  // Add legend to the nodes list if doesn't exist.
  var add_legend = currInd > 0 &&
                 $( '.slick-active .org-chart_legend' ).length === 0;
  if ( add_legend ) {
    $( '.slick-active > .org-chart_nodes' ).append( $legend );
  }

  _updateHeight();
  _initExpandables();
}

function _destroySlider() {
  // Destroy slider.
  if ( _slider ) { _slider.destroy(); }
  _slider = null;
  // Hide content slider & mobile nav links.
  $( '#content-slider, .content-hide' ).hide();
  // Show org chart branches.
  $( '.org-chart_branches' ).show();

  for ( var i = 0, len = _expandables.length; i < len; i++ ) {
    _expandables[i].removeEventListener( 'expandEnd', _updateHeight );
    _expandables[i].removeEventListener( 'collapseEnd', _updateHeight );
    _expandables[i].destroy();
  }
}

init();
