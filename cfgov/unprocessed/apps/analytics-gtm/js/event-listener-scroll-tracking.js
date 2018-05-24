import { analyticsLog } from './util/analytics-util';

// Default time delay before checking location.
const callBackTime = 100;

// Number of pixels before tracking a reader.
const readerLocation = 200;

// Set some flags for tracking & execution.
let timer = 0;
let hasStartScroll = false;

/* Threshold of pixels at bottomPos when 100% triggers.
   For some reason some monitors were found to be a pixel off when scrolling to the bottomPos,
   this gives a little wiggle-room for when the 100% event fires
   so that it'll be 5px or less from the bottomPos. */
const threshold = 5;

const viewableHeight = window.innerHeight;
const totalheight = document.body.offsetHeight - threshold;
const totalHiddenHeight = totalheight - viewableHeight;

// This will record events so they only fire once.
const hasFired = {};

// This will store the y-position of the breakpoints at which to fire events.
const yPosCache = {};

// Set some time variables to calculate reading time.
const startTime = new Date();
const timeAtPageLoad = startTime.getTime();

/**
 * @returns {number} Seconds that have elapsed since the page load time.
 */
function getTimeStamp() {
  const currentTime = new Date();
  return Math.round( ( currentTime.getTime() - timeAtPageLoad ) / 1000 );
}

/**
 * [trackSpecificLocation description]
 * @param {number} bottomPos -
 *   Number of pixels from the top of the page to current scroll top position.
 * @param {number} percent - Percent of the scrollable height to fire from.
 */
function trackSpecificLocation( bottomPos, percent ) {
  let yPos = yPosCache[percent];

  if ( !yPos ) {
    const percentAsDecimal = percent / 100;
    yPos = ( totalHiddenHeight * percentAsDecimal ) + viewableHeight;
    yPosCache[percent] = yPos;
  }

  const hasFiredID = `hit${ percent }`;

  if ( !hasFired[hasFiredID] && bottomPos >= yPos ) {
    const timeToContentEnd = getTimeStamp();

    window.dataLayer.push( {
      event: 'scrollEvent',
      scrollProgress: `${ percent }%`,
      scrollTime: timeToContentEnd
    } );
    analyticsLog(
      `Scrolled ${ percent }% of hidden height ` +
      `${ timeToContentEnd }s after page load.`
    );

    hasFired[hasFiredID] = true;
  }
}

// Check the location and track user
function trackLocation() {
  const bottomPos = viewableHeight + document.documentElement.scrollTop;

  // If user starts to scroll send an event, currently disabled
  if ( bottomPos > readerLocation && !hasStartScroll ) {
    const timeToScroll = getTimeStamp();

    /* window.dataLayer.push({'event':'scrollEvent',
       scrollProgress: 'start-scroll',
       scrollTime: timeToScroll}); */
    analyticsLog( `Started scrolling ${ timeToScroll }s after page load.` );

    hasStartScroll = true;
  }

  // If user has hit 25%, currently disabled.
  trackSpecificLocation( bottomPos, 25 );

  // If user has hit 50%.
  trackSpecificLocation( bottomPos, 50 );

  // If user has hit 75%, currently disabled.
  trackSpecificLocation( bottomPos, 75 );

  // If user has hit 100%.
  trackSpecificLocation( bottomPos, 100 );
}

// Track the scrolling and track location
window.addEventListener( 'scroll', function() {
  if ( timer ) {
    clearTimeout( timer );
  }
  // Use a buffer so we don't call trackLocation too often.
  timer = setTimeout( trackLocation, callBackTime );
} );
