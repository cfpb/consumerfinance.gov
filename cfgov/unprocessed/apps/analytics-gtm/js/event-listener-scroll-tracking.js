import $ from 'jquery';

// Debug flag - set this to true to send console logs instead of dataLayer pushes.
const debugMode = false;

// Default time delay before checking location.
const callBackTime = 100;

// Number of pixels before tracking a reader.
const readerLocation = 200;

// Set some flags for tracking & execution.
let timer = 0;
let scroller = false;
const didComplete = false;

// Set some time variables to calculate reading time.
const startTime = new Date();
const beginning = startTime.getTime();
const totalTime = 0;

/* Threshold of pixels at bottom when 100% triggers.
   For some reason some monitors were found to be a pixel off when scrolling to the bottom,
   this gives a little wiggle-room for when the 100% event fires
   so that it'll be 5px or less from the bottom. */
const threshold = 5;

const totalheight = document.body.offsetHeight - threshold;

// These will make sure the events only fire once.
let hit25 = false;
let hit50 = false;
let hit75 = false;
let hit100 = false;

const y100 = totalheight; // End of page.
const y25 = y100 * 0.25; // Breakpoint 25%.
const y50 = y100 * 0.50; // Breakpoint 50%.
const y75 = y100 * 0.75; // Breakpoint 75%.

// Check if the window is bigger than the scrollpoints.
if ( y50 < window.innerHeight ) {
  hit50 = true;
}

if ( y100 < window.innerHeight ) {
  hit100 = true;
}

// Check the location and track user
function trackLocation() {
  const bottom = window.innerHeight + document.body.scrollTop;
  let currentTime;
  let scrollStart;
  let timeToScroll;
  let contentScrollEnd;
  let timeToContentEnd;

  // If user starts to scroll send an event, currently disabled
  if ( bottom > readerLocation && !scroller ) {
    currentTime = new Date();
    scrollStart = currentTime.getTime();
    timeToScroll = Math.round( ( scrollStart - beginning ) / 1000 );
    if ( debugMode ) {
      /* window.dataLayer.push({'event':'scrollEvent',
         'scrollProgress':'start-scroll',
         'scrollTime':timeToScroll}); */
    } else {
      console.log( 'started scrolling ' + timeToScroll );
    }
    scroller = true;
  }
  // If user has hit 25%, currently disabled
  if ( bottom >= y25 && hit25 === false ) {
    currentTime = new Date();
    contentScrollEnd = currentTime.getTime();
    timeToContentEnd = Math.round( ( contentScrollEnd - scrollStart ) / 1000 );
    if ( debugMode ) {
      console.log( 'hit 25% ' + timeToContentEnd );
    } else {
      /* window.dataLayer.push({'event':'scrollEvent',
         'scrollProgress':'25%',
         'scrollTime':timeToContentEnd}); */
    }
    hit25 = true;
  }
  // If user has hit 50%
  if ( bottom >= y50 && hit50 === false ) {
    currentTime = new Date();
    contentScrollEnd = currentTime.getTime();
    timeToContentEnd = Math.round( ( contentScrollEnd - scrollStart ) / 1000 );
    if ( debugMode ) {
      console.log( 'hit 50% ' + timeToContentEnd );
    } else {
      window.dataLayer.push( {
        event: 'scrollEvent',
        scrollProgress: '50%',
        scrollTime: timeToContentEnd
      } );
    }
    hit50 = true;
  }
  // If user has hit 75%, currently disabled
  if ( bottom >= y75 && hit75 === false ) {
    currentTime = new Date();
    contentScrollEnd = currentTime.getTime();
    timeToContentEnd = Math.round( ( contentScrollEnd - scrollStart ) / 1000 );
    if ( debugMode ) {
      console.log( 'hit 75% ' + timeToContentEnd );
    } else {
      /* window.dataLayer.push({'event':'scrollEvent',
         'scrollProgress':'75%',
         'scrollTime':timeToContentEnd}); */
    }
    hit75 = true;
  }
  // If user has hit 100%
  if ( bottom >= y100 && hit100 === false ) {
    currentTime = new Date();
    contentScrollEnd = currentTime.getTime();
    timeToContentEnd = Math.round( ( contentScrollEnd - scrollStart ) / 1000 );
    if ( debugMode ) {
      window.dataLayer.push( {
        event: 'scrollEvent',
        scrollProgress: '100%',
        scrollTime: timeToContentEnd
      } );
    } else {
      console.log( 'hit 100% ' + timeToContentEnd );
    }
    hit100 = true;
  }
}
// Track the scrolling and track location
window.addEventListener( 'scroll', function() {
  if ( timer ) {
    clearTimeout( timer );
  }
  // Use a buffer so we don't call trackLocation too often.
  timer = setTimeout( trackLocation, callBackTime );
} );
