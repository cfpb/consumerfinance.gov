/* ==========================================================================
   Utility to capture a screenshot of the current browser window.
   ========================================================================== */

'use strict';

var fs = require( 'fs' );

var _screenShotDirectory = 'test/';

/**
 * Write a screenshot string to a file.
 * @param {string} filename - The filename of the file to create.
 * @param {string} data - A base64-encoded string to write to a file.
 */
function _writeScreenShot( filename, data ) {
  var stream = fs.createWriteStream( _screenShotDirectory + filename );

  stream.write( new Buffer( data, 'base64' ) );
  stream.end();
}

/**
 * Process a screenshot generated from a browser.takeScreenshot() promise.
 * @param {string} png - A base64-encoded string to write to a file.
 */
function _processScreenshot( png ) {
  _writeScreenShot( 'screenshot.png', png );
}

/**
 * Capture a screenshot of the current browser window.
 */
function capture() {
  browser.takeScreenshot().then( _processScreenshot );
}

// Expose public methods.
module.exports = { capture: capture };
