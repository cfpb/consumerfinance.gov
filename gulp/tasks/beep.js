'use strict';

var fs = require( 'fs' );
var gulp = require( 'gulp' );
var path = require( 'path' );
var Player;

// See that the player module has loaded.
// If this is run on TravisCI it will not have loaded
// and the rest of the code goes through its normal error handling.
/* eslint-disable global-require, handle-callback-err, no-console, lines-around-comment, max-len */
try {
  Player = require( 'player' );
} catch ( err ) {
  console.log( 'Warning: NPM Player module did not load!' );
}
/* eslint-enable */

var SONG_PATH = 'beep-build.mp3';

/**
 * Play an mp3 file using the Player npm module.
 * @param {string} soundPath The path to a sound file.
 */
function _playSound( soundPath ) {
  var player = new Player( soundPath );
  player.play();

  player.on( 'error', function() { // eslint-disable-line handle-callback-err, no-inline-comments, max-len
    // Ignore playback errors because
    // it's not critical if the beep doesn't play.
  } );
}

gulp.task( 'beep', function() {

  try {
    var soundPath = path.join( __dirname, '../../' + SONG_PATH );
    var stats = fs.lstatSync( soundPath ); // eslint-disable-line no-sync, no-inline-comments, max-len
    if ( stats.isFile() ) {
      _playSound( soundPath );
    }
  } catch ( err ) {
    console.log( 'No build alert beep configured. Add a sound file as "' + // eslint-disable-line no-console, no-inline-comments, max-len
                 SONG_PATH + '" in the project root directory.' );
  }
} );
