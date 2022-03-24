const { readdir, mkdir, copyFile } = require( 'fs' ).promises;
const { resolve, dirname } = require( 'path' );
const { unprocessed, modules } = require( '../config/environment.js' ).paths;

const rDir = resolve( '.' );
const blacklist = [
  'node_modules', 'npm-packages-offline-cache', '.yarnrc', 'yarn.lock',
  'browserslist', 'package.json', 'config.json', '.gitkeep', 'root'
];

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

module.exports = async function( baseConfig ) {
  const files = await getFiles( unprocessed );
  const staticFiles = files.filter( v => !v.match( /.js$|.less$|.css$/ ) );
  const inDirs = [ ...new Set( staticFiles.map( v => dirname( v ) ) ) ];
  const outDirs = [
    ...inDirs.map( v => v.replace( unprocessed, baseConfig.outdir ) ),
    // Hande prebuilt lightbox dep
    ...[ '', '/images', '/js', '/css' ]
      .map( v => `${ baseConfig.outdir }/lightbox2${ v }` )
  ];

  // Make output directories
  await Promise.all( outDirs.map( d => mkdir( d, { recursive: true } ) ) );

  // Copy files to output directories
  await Promise.all( staticFiles.map( f => copyFile(
    f, f.replace( unprocessed, baseConfig.outdir )
  ) ) );

  // Handle prebuilt lightbox dep
  await Promise.all( [
    `${ modules }/lightbox2/dist/css/lightbox.min.css`,
    `${ modules }/lightbox2/dist/images/close.png`,
    `${ modules }/lightbox2/dist/images/loading.gif`,
    `${ modules }/lightbox2/dist/images/next.png`,
    `${ modules }/lightbox2/dist/images/prev.png`,
    `${ modules }/lightbox2/dist/js/lightbox-plus-jquery.min.js`
  ].map( f => copyFile(
    f, f.replace(
      `${ modules }/lightbox2/dist`,
      `${ baseConfig.outdir }/lightbox2`
    ) ) )
  );
};
