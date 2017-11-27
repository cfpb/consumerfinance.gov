/* ==========================================================================
   Provides utilities for returning a list of per-page JS files
   for consumption by a script loader.
   ========================================================================== */

'use strict';

const fs = require( 'fs' );

const _sourcePathCache = {};

/**
 * Traverse a directory and return an object with keys
 * and values equal to the files in the directory tree.
 * @param {string} dir Directory to traverse.
 * @param {Object} list An object that is used to compile the list of files.
 *   Should start empty.
 * @param {string} baseDir The base directory the traversal started from.
 * @returns {Object}
 *   Hash with keys and values equal to the files in the directory tree.
 */
function _traverseDirectory( dir, list, baseDir ) {
  if ( !baseDir ) { baseDir = dir; }
  const stats = fs.lstatSync( dir ); // eslint-disable-line no-sync, no-inline-comments, max-len
  if ( stats.isDirectory() ) {
    fs.readdirSync( dir ).map( function( child ) { // eslint-disable-line no-sync, no-inline-comments, max-len
      return _traverseDirectory( dir + '/' + child, list, baseDir );
    } );
  } else if ( !_isHidden( dir ) ) {
    const relativePath = dir.substring( baseDir.length + 1 );
    list[relativePath] = './' + relativePath;
  }

  return list;
}

/**
 * Checks whether a file path contains a hidden file or a folder.
 * @param {string} path Filepath to check.
 * @returns {boolean} true if the source is hidden, otherwise false.
 */
function _isHidden( path ) {
  return ( /(^|\/)\.[^/.]/g ).test( path );
}

/**
 * Retrieve a directory tree hash map from cache
 *   or traverse the given directory and create and return a new cache.
 * @param {string} dir Directory to traverse.
 * @returns {Object}
 *   Hash with keys and values equal to the files in the directory tree.
 */
function getDirectoryMap( dir ) {
  let cache = _sourcePathCache[dir];
  if ( !_sourcePathCache[dir] ) {
    var directoryMap = _traverseDirectory( dir, {} );
    _sourcePathCache[dir] = directoryMap;
    cache = directoryMap;
  }
  return cache;
}

module.exports = {
  getDirectoryMap: getDirectoryMap
};
