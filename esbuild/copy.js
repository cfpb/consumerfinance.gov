const { mkdir, copyFile } = require( 'fs' ).promises;
const { dirname, resolve } = require( 'path' );
const { getFiles, copyAll } = require( './utils.js' );
const { unprocessed, modules } = require( '../config/environment.js' ).paths;

module.exports = async function( baseConfig ) {
  const resolvedBase = resolve( unprocessed );
  const files = await getFiles( resolvedBase );

  const staticFiles = files.filter( v => !v.match( /\/\.[-.\w]*$|\.js$|\.less$|\.css$/i ) );

  const inDirs = [
    ...new Set( staticFiles.map( v => dirname( v ) ) )
  ];

  const outDirs = [
    ...inDirs.map( v => v.replace( resolvedBase, baseConfig.outdir ) ),
    // Create specific icon directory
    `${ baseConfig.outdir }/icons`
  ];

  // Make output directories
  await Promise.all( outDirs.map( d => mkdir( d, { recursive: true } ) ) );

  // Copy files to output directories
  staticFiles.forEach( f => copyFile(
    f, f.replace( resolvedBase, baseConfig.outdir )
  ) );

  // Handle files that live at the root of the site
  copyAll( `${ unprocessed }/root`, baseConfig.outdir );

  // Handle icons
  copyAll( `${ modules }/@cfpb/cfpb-icons/src/icons`, `${ baseConfig.outdir }/icons` );
};
