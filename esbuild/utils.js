const { readdirSync } = require( 'fs' );

/**
 * @param {string} path The directory with the needed js
 * @param {regex} regex The regex to match against
 * @returns {array} An array of matched files
 */
function getAll( path, regex = /.js$/ ) {
  return readdirSync( path )
    .filter( v => v.match( regex ) )
    .map( v => `${ path }/${ v }` );
}

module.exports = { getAll };
