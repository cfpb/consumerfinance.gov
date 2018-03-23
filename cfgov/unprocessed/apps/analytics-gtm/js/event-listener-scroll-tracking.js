// Debug flag - set this to true to send console logs instead of dataLayer pushes.
var debugMode = false;

// Default time delay before checking location.
var callBackTime = 100;

// Number of pixels before tracking a reader.
var readerLocation = 200;

// Set some flags for tracking & execution.
var timer = 0;
var scroller = false;
var didComplete = false;

// Set some time variables to calculate reading time.
var startTime = new Date();
var beginning = startTime.getTime();
var totalTime = 0;

// Threshold of pixels at bottom when 100% triggers.
// For some reason some monitors were found to be a pixel off when scrolling to the bottom,
// this gives a little wiggle-room for when the 100% event fires
// so that it'll be 5px or less from the bottom.
var threshold = 5;

var totalheight = document.body.offsetHeight - threshold;

// These will make sure the events only fire once.
var hit25 = false;
var hit50 = false;
var hit75 = false;
var hit100 = false;

var y100 = totalheight; // End of page.
var y25 = y100 * 0.25;  // Breakpoint 25%.
var y50 = y100 * 0.50;  // Breakpoint 50%.
var y75 = y100 * 0.75;  // Breakpoint 75%.

// Check if the window is bigger than the scrollpoints.
if ( y50 < window.innerHeight ) {
  hit50 = true;
}

if ( y100 < window.innerHeight ) {
  hit100 = true;
}

// Check the location and track user
function trackLocation() {
  bottom = window.innerHeight + document.body.scrollTop;

    // If user starts to scroll send an event, currently disabled
  if (bottom > readerLocation && !scroller) {
    currentTime = new Date();
    scrollStart = currentTime.getTime();
    timeToScroll = Math.round((scrollStart - beginning) / 1000);
    if (!debugMode) {
      //  dataLayer.push({'event':'scrollEvent',
      // 'scrollProgress':'start-scroll',
      // 'scrollTime':timeToScroll});
    }
    else {
      console.log('started scrolling ' + timeToScroll);
    }
    scroller = true;
  }
    // If user has hit 25%, currently disabled
  if (bottom >= y25 && hit25 == false) {
    currentTime = new Date();
    contentScrollEnd = currentTime.getTime();
    timeToContentEnd = Math.round((contentScrollEnd - scrollStart) / 1000);
    if (!debugMode) {
      //  dataLayer.push({'event':'scrollEvent',
      // 'scrollProgress':'25%',
      // 'scrollTime':timeToContentEnd});
    }
    else {
      console.log('hit 25% '+ timeToContentEnd);
    }
    hit25 = true;
  }
  // If user has hit 50%
  if (bottom >= y50 && hit50 == false ) {
    currentTime = new Date();
    contentScrollEnd = currentTime.getTime();
    timeToContentEnd = Math.round((contentScrollEnd - scrollStart) / 1000);
    if (!debugMode) {
       dataLayer.push({
         'event':'scrollEvent',
         'scrollProgress':'50%',
         'scrollTime':timeToContentEnd
       });
    }
    else {
      console.log('hit 50% '+ timeToContentEnd);
    }
    hit50 = true
  }
    // If user has hit 75%, currently disabled
  if (bottom >= y75 && hit75 == false) {
    currentTime = new Date();
    contentScrollEnd = currentTime.getTime();
    timeToContentEnd = Math.round((contentScrollEnd - scrollStart) / 1000);
    if (!debugMode) {
      // dataLayer.push({'event':'scrollEvent',
      // 'scrollProgress':'75%',
      // 'scrollTime':timeToContentEnd});
    }
    else {
      console.log('hit 75% '+ timeToContentEnd);
    }
    hit75 = true;
  }
    // If user has hit 100%
  if (bottom >= y100 && hit100 == false) {
    currentTime = new Date();
    contentScrollEnd = currentTime.getTime();
    timeToContentEnd = Math.round((contentScrollEnd - scrollStart) / 1000);
    if (!debugMode) {
      dataLayer.push({
        'event':'scrollEvent',
        'scrollProgress':'100%',
        'scrollTime':timeToContentEnd
      });
    }
    else {
      console.log('hit 100% '+ timeToContentEnd);
    }
    hit100 = true;
  }
}
// Track the scrolling and track location
window.addEventListener('scroll', function() {
  if (timer) {
    clearTimeout(timer);
  }
  // Use a buffer so we don't call trackLocation too often.
  timer = setTimeout(trackLocation, callBackTime);
});
