/* ==========================================================================
   Homepage
   Scripts for the main landing page of the site.
   ========================================================================== */

'use strict';

window.requestNextAnimationFrame = require( 'requestNextAnimationFrame' );

// Multiplier determines how pixel dense the canvas should be.
// This way canvas can look good even on retina displays.
var multiplier = 2;

// Boolean to end the animation loop so it's not just running continuously in the background.
var animationComplete = false;

// This variable keeps track of time by counting the number of frames drawn.
var iterationCount = 0;

var radius = ( $( '.progress-charts_container' ).width() * multiplier ) / 2,
    arcStart = 270,
    center = {
      x: radius,
      y: radius
    };

// Array of objects to store each chart's values.
var charts = [
  {
    name:  'consumer guides',
    done:  parseInt( $( '#consumer-guides .chart-value' ).text(), 10 ) / 100,
    value: 0
  },
  {
    name:  'submit a complaint',
    done:  parseInt( $( '#submit-a-complaint .chart-value' ).text(), 10 ) / 100,
    value: 0
  },
  {
    name:  'data and research',
    done:  parseInt( $( '#data-and-research .chart-value' ).text(), 10 ) / 100,
    value: 0
  },
  {
    name:  'policy and compliance',
    done:  parseInt( $( '#policy-and-compliance .chart-value' ).text(), 10 ) / 100,
    value: 0
  },
  {
    name:  'about',
    done:  parseInt( $( '#about .chart-value' ).text(), 10 ) / 100,
    value: 0
  }
];

// Set up each canvas element.
$( '.progress-charts_chart' ).each( function() {
  var ctx = $( this )[0].getContext( '2d' );
  ctx.canvas.width = $( '.progress-charts_container' ).width() * multiplier;
  ctx.canvas.height = ctx.canvas.width;
} );

// Run everything on load (or switch to when in view).
$( document ).ready( function() {
  if ( !animationComplete ) {
    animate();
  }
} );

function animate() {
  // Variable to keep track of when all charts are finished animating.
  var completeCount = 0;
  $( '.progress-charts_chart' ).each( function( i ) {
    // snag the context
    var ctx = $( this )[0].getContext( '2d' );
    if ( charts[i].value < charts[i].done ) {
      // ease the value (90 being how long it should take)
      // we're animating at 60fps so 90 is 1.5 seconds
      charts[i].value = easeInOutQuint( iterationCount, 0, charts[i].done, 90 );
    } else {
      completeCount++;
    }
    // send values to be drawn
    drawGraph( ctx, charts[i].value );
  });
  // each loop through is a animation frame, so count up the frames
  iterationCount++;
  // if charts aren't finished animating, loop again
  if ( completeCount < 5 ) {
    window.requestNextAnimationFrame( animate );
  } else {
    animationComplete = true;
  }
}

function drawGraph( context, value ) {
  context.clearRect( 0, 0, context.canvas.width, context.canvas.height );
  // inner grey
  context.beginPath();
  context.arc( center.x, center.y, radius - ( 4 * multiplier ), 0, 2 * Math.PI );
  context.fillStyle = '#E3E4E5';
  context.fill();

  var pct;
  if ( value < 1 ) {
    // decimal 0.0 - 1 for percentage
    pct = arcStart + ( value * 360 );
    // fill percentage arc
    context.beginPath();
    context.moveTo( center.x, center.y );
    context.arc( center.x, center.y, radius, getRadians(arcStart), getRadians( pct ), false );
    context.closePath();
    context.fillStyle = '#FF931B';
    context.fill();
    // center circle
    context.beginPath();
    context.arc( center.x, center.y, radius / 1.85, 0, 2 * Math.PI );
    context.fillStyle = '#FFF';
    context.fill();
  } else { // switch to green
    // decimal 0.0 - 1 for percentage
    pct = arcStart + ( value * 360 );
    // fill percentage arc
    context.beginPath();
    context.moveTo( center.x, center.y );
    context.arc( center.x, center.y, radius, getRadians( arcStart ), getRadians( pct ), false );
    context.closePath();
    context.fillStyle = '#2CB34A';
    context.fill();
    // center circle
    context.beginPath();
    context.arc(center.x, center.y, radius / 1.85, 0, 2 * Math.PI);
    context.fillStyle = '#ADDC91';
    context.fill();
    // check mark
    var unit = ( radius - (4 * multiplier) ) / 5;
    context.beginPath();
    context.moveTo(center.x - unit, center.y);
    context.lineTo(center.x - unit / 2, center.y + unit);
    context.lineWidth = 6 * (radius / 100) * multiplier;
    context.strokeStyle = '#FFF';
    context.lineCap = 'round';
    context.stroke();
    context.beginPath();
    context.moveTo(center.x - unit / 2, center.y + unit);
    context.lineTo(center.x + unit, center.y - unit);
    context.stroke();
  }
}


// ------------------------------------------------
// Utilities
// ------------------------------------------------

function getRadians( degrees ) {
  return degrees * Math.PI / 180;
}

function easeInOutQuint( currentIteration, startValue, changeInValue, totalIterations ) {
  if ( (currentIteration /= totalIterations / 2) < 1) {
    return changeInValue / 2 * Math.pow( currentIteration, 5 ) + startValue;
  }
  return changeInValue / 2 * (Math.pow( currentIteration - 2, 5 ) + 2) + startValue;
}

// wait for timer
var waitForFinalEvent = ( function () {
  var timers = {};
  return function ( callback, ms, uniqueId ) {
    if ( !uniqueId ) {
      uniqueId = "Don't call this twice without a uniqueId";
    }
    if ( timers[uniqueId] ) {
      clearTimeout( timers[uniqueId] );
    }
    timers[uniqueId] = setTimeout(callback, ms);
  };
} )();


// ------------------------------------------------
// Events
// ------------------------------------------------

$( window ).resize( function() {
  // Reset after resize (just in case).
  waitForFinalEvent();
} );
