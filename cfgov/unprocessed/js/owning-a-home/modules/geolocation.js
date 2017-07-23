'use strict';

var guessState = require( 'fuzzy-state-search' );
var UNDEFINED;

module.exports.getState = function( options, callback ) {

  if ( !window.navigator.geolocation ) {
    var closestState = { name: 'AL' };

    return closestState;
  }

  var opts = options || {};
  var timeout = opts.timeout || 10000;
  var cb = typeof options === 'function' ? options : callback;
  var reallyIndecisive = true;

  function success( pos ) {
    var state = guessState( pos );
    reallyIndecisive = false;
    if ( cb ) {
      return cb( state );
    }

    return UNDEFINED;
  }

  function fail() {
    return cb();
  }

  // Get their state using the HTML5 gelocation API.
  navigator.geolocation.getCurrentPosition( success, fail );

  // For users who don't see the geolocate permission bar in their
  // browser, fail after X milliseconds.
  setTimeout( function() {
    if ( reallyIndecisive ) {
      fail();
    }
  }, timeout );

  return UNDEFINED;
};
