const { readdir, copyFile } = require( 'fs' ).promises;
const { readdirSync } = require( 'fs' );
const { resolve } = require( 'path' );

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

// Files that should not be copied and directories that should not be walked
const blacklist = [
  'node_modules', 'npm-packages-offline-cache', '.yarnrc', 'yarn.lock',
  'browserslist', 'package.json', 'config.json', '.gitkeep', 'root'
];
const rDir = resolve( '.' );

/**
 * @param {string} dir Current directory to walk
**/
async function getFiles( dir ) {
  const dirents = await readdir( dir, { withFileTypes: true } );
  const files = await Promise.all( dirents.map( dirent => {
    if ( blacklist.indexOf( dirent.name ) > -1 ) return '';
    const res = resolve( dir, dirent.name );
    return dirent.isDirectory() ? getFiles( res ) : res;
  } ) );
  return files.flat().filter( v => v )
    .map( v => v.replace( rDir, '.' ) );
}

/**
 * @param {string} from Directory to copy files from
 * @param {string} to Directory to copy files to
 * @returns {array} Array of promises for each copied file
 **/
async function copyAll( from, to ) {
  const files = await getFiles( from );
  return files.map( f => copyFile(
    f, f.replace( from, to )
  ) );
}


module.exports = { getAll, getFiles, copyAll };
