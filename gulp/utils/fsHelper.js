'use strict';

var path = require( 'path' );

/**
 * Retrieve a reference path to a binary.
 * @param {string} binaryName The name of the binary to retrieve.
 * @param {string} binaryDir The name of the binary directory to use.
 *   `bin` by default.
 * @returns {string} Path to the binary to run.
 */
function getBinary( binaryName, binaryDir ) {
  binaryDir = binaryDir || 'bin';
  var winExt = ( /^win/ ).test( process.platform ) ? '.cmd' : '';
  var pkgPath = require.resolve( binaryName );
  binaryDir = path.resolve(
    path.join( path.dirname( pkgPath ), '..', binaryDir )
  );
  return path.join( binaryDir, '/' + binaryName + winExt );
}

module.exports = {
  getBinary: getBinary
};
