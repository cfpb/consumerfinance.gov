/* ==========================================================================
   Homepage
   Scripts for the main landing page of the site.
   ========================================================================== */

'use strict';

var $ = require( 'jquery' );

// Multiplier determines how pixel dense the canvas should be.
// This way canvas can look good even on retina displays.
var _multiplier = 2;

// This variable keeps track of time by counting the number of frames drawn.
var _iterationCount = 0;

// Variable to keep track of when all charts are finished animating.
var _completeCount = 0;

var _$chartsDom;
var _charts;
var _center;
var _radius;
var _arcStart;

/**
 * Initialize the progress bars if requestAnimationFrame is supported.
 */
function init() {
  var chartsContainerDom = document.querySelector( '.project-progress' );
  if ( _requestAnimationFrameSupported() && chartsContainerDom ) {
    // Classlist not supported on <IE9 and Opera Mini,
    // but neither is requestAnimationFrame, so usage here is okay.
    chartsContainerDom.classList.remove( 'u-hidden' );
  } else {
    return;
  }

  var $chartsContainerDom = $( '.progress-charts_container' );

  _radius = $chartsContainerDom.width() * _multiplier / 2;
  _arcStart = 270;
  _center = {
    x: _radius,
    y: _radius
  };

  // Array of objects to store each chart's values.
  _charts = _buildCharts();

  _$chartsDom = $( '.progress-charts_chart' );

  // Set up each canvas element.
  _$chartsDom.each( function() {
    var ctx = $( this )[0].getContext( '2d' );
    ctx.canvas.width = $chartsContainerDom.width() * _multiplier;
    ctx.canvas.height = ctx.canvas.width;
  } );

  _animate();
}

/**
 * Build the source charts data based on the value set in the text in the DOM.
 * @returns {Array} List of objects with done and value settings corresponding
 *   to each graph item, where done is the total amount to draw,
 *   and value is where to start animating from.
 */
function _buildCharts() {
  var chartsValueSelector = '.progress-charts_container .chart-value';
  var chartsDom = document.querySelectorAll( chartsValueSelector );
  var charts = [];
  var chartItem;
  var doneValue;

  for ( var i = 0, len = chartsDom.length; i < len; i++ ) {
    chartItem = chartsDom[i];
    doneValue = parseInt( chartItem.innerText || chartItem.textContent, 10 );
    charts.push( {
      done:  doneValue / 100,
      value: 0
    } );
  }

  return charts;
}

/**
 * @returns {boolean} Whether requestAnimationFrame is supported or not.
 */
function _requestAnimationFrameSupported() { // eslint-disable-line
  // Has a complexity of 5 (ESLint complexity violation), but it's OK.
  var isSupported = window.requestAnimationFrame ||
                    window.webkitRequestAnimationFrame ||
                    window.mozRequestAnimationFrame ||
                    window.oRequestAnimationFrame ||
                    window.msRequestAnimationFrame;
  return isSupported;
}

/**
 * Animate drawing of the arcs.
 */
function _animate() {
  _completeCount = 0;
  _$chartsDom.each( _drawAnimationFrame );

  // Each loop through is an animation frame, so count up the frames.
  _iterationCount++;

  // If charts aren't finished animating, loop again.
  if ( _completeCount < 5 ) {
    window.requestAnimationFrame( _animate );
  }
}

/**
 * Draw an step of the arc drawing animation.
 * @param {Object} i The chart item to draw.
 */
function _drawAnimationFrame( i ) {
  // Snag the context.
  var ctx = $( this )[0].getContext( '2d' );
  if ( _charts[i].value < _charts[i].done ) {
    // Ease the value (90 being how long it should take)
    // we're animating at 60fps so 90 is 1.5 seconds.
    _charts[i].value = _easeInOutQuint( _iterationCount, 0,
                                        _charts[i].done, 90 );
  } else {
    _completeCount++;
  }
  // Send values to be drawn.
  _drawGraph( ctx, _charts[i].value );
}

/**
 * Draw the graph arc.
 * @param {Object} context A 2d canvas context.
 * @param {number} value The percentage done value of the arc to draw.
 */
function _drawGraph( context, value ) {
  context.clearRect( 0, 0, context.canvas.width, context.canvas.height );
  // inner grey
  _drawInnerCircle( context, '#E3E4E5' );

  if ( value < 1 ) {
    _drawProgressArc( context, '#FF931B', value );
  } else {
    _drawFinalArc( context, '#2CB34A', '#ADDC91' );
  }
}

/**
 * Draw the inner circle of the graph arc.
 * @param {Object} context A 2d canvas context.
 * @param {string} color A hex color value.
 */
function _drawInnerCircle( context, color ) {
  context.beginPath();
  context.arc( _center.x, _center.y, _radius - 4 * _multiplier,
               0, 2 * Math.PI );
  context.fillStyle = color;
  context.fill();
}

/**
 * Draw the inner circle of the graph arc.
 * @param {Object} context A 2d canvas context.
 * @param {string} color A hex color value.
 * @param {number} value The percentage done value of the arc to draw.
 */
function _drawProgressArc( context, color, value ) {
  // Decimal 0.0 - 1 for percentage filled.
  var pct = _arcStart + value * 360;
  // Draw outer fill percentage arc.
  context.beginPath();
  context.moveTo( _center.x, _center.y );
  context.arc( _center.x, _center.y, _radius,
               _getRadians( _arcStart ), _getRadians( pct ), false );
  context.closePath();
  context.fillStyle = color;
  context.fill();
  // Draw inner circle.
  context.beginPath();
  context.arc( _center.x, _center.y, _radius / 1.85, 0, 2 * Math.PI );
  context.fillStyle = '#FFF';
  context.fill();
}

/**
 * Draw the inner circle of the graph arc.
 * @param {Object} context A 2d canvas context.
 * @param {string} outerColor A hex color value for the outer arc.
 * @param {string} innerColor A hex color value for the inner arc circle.
 */
function _drawFinalArc( context, outerColor, innerColor ) {
  // Draw outer fill percentage arc.
  context.beginPath();
  context.moveTo( _center.x, _center.y );
  context.arc( _center.x, _center.y, _radius,
               0, _getRadians( 360 ), false );
  context.closePath();
  context.fillStyle = outerColor;
  context.fill();
  // Draw inner circle.
  context.beginPath();
  context.arc( _center.x, _center.y, _radius / 1.85, 0, 2 * Math.PI );
  context.fillStyle = innerColor;
  context.fill();
  // Draw check mark.
  var unit = ( _radius - 4 * _multiplier ) / 5;
  context.beginPath();
  context.moveTo( _center.x - unit, _center.y );
  context.lineTo( _center.x - unit / 2, _center.y + unit );
  context.lineWidth = 6 * ( _radius / 100 ) * _multiplier;
  context.strokeStyle = '#FFF';
  context.lineCap = 'round';
  context.stroke();
  context.beginPath();
  context.moveTo( _center.x - unit / 2, _center.y + unit );
  context.lineTo( _center.x + unit, _center.y - unit );
  context.stroke();
}

/**
 * @param {number} degrees Degrees to convert to radians.
 * @returns {string} Degrees converted to radians.
 */
function _getRadians( degrees ) {
  return degrees * Math.PI / 180;
}

/**
 * @param {number} currentIteration Current step in an animation.
 * @param {number} startValue Starting value over the course of an animation.
 * @param {number} changeInValue Final value over the course of an animation.
 * @param {number} totalIterations Total steps in an animation.
 * @returns {number} Current value at this point in the iteration.
 */
function _easeInOutQuint( currentIteration, startValue,
                          changeInValue, totalIterations ) {
  if ( ( currentIteration /= totalIterations / 2 ) < 1 ) {
    return changeInValue / 2 *
           Math.pow( currentIteration, 5 ) + startValue;
  }
  return changeInValue / 2 *
         ( Math.pow( currentIteration - 2, 5 ) + 2 ) + startValue;
}

module.exports = { init: init };
