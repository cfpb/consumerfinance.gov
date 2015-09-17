'use strict';

var path = require( 'path' );

/**
 * Retrieve a reference path to a binary.
 * @param {string} binaryName The name of the binary to retrieve.
 * @returns {string} Path to the binary to run.
 */
function getBinary( binaryName ) {
  var winExt = ( /^win/ ).test( process.platform ) ? '.cmd' : '';
  var pkgPath = require.resolve( binaryName );
  var binaryDir = path.resolve(
    path.join( path.dirname( pkgPath ), '..', 'bin' )
  );
  return path.join( binaryDir, '/' + binaryName + winExt );
}

module.exports = {
  getBinary: getBinary
};
