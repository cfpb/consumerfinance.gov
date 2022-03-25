const { mkdir, copyFile } = require( 'fs' ).promises;
const { dirname } = require( 'path' );
const { getFiles, copyAll } = require( './utils.js' );
const { unprocessed, modules } = require( '../config/environment.js' ).paths;

module.exports = async function( baseConfig ) {
  const files = await getFiles( unprocessed );
  const staticFiles = files.filter( v => !v.match( /.js$|.less$|.css$/ ) );

  const inDirs = [ ...new Set( staticFiles.map( v => dirname( v ) ) ) ];
  const outDirs = [
    ...inDirs.map( v => v.replace( unprocessed, baseConfig.outdir ) ),
    // Create specific icon directory
    `${ baseConfig.outdir }/icons`,
    // Hande prebuilt lightbox dep
    ...[ '', '/images', '/js', '/css' ]
      .map( v => `${ baseConfig.outdir }/lightbox2${ v }` )
  ];

  // Make output directories
  await Promise.all( outDirs.map( d => mkdir( d, { recursive: true } ) ) );

  // Copy files to output directories
  staticFiles.forEach( f => copyFile(
    f, f.replace( unprocessed, baseConfig.outdir )
  ) );

  // Handle files that live at the root of the site
  copyAll( `${ unprocessed }/root`, baseConfig.outdir );

  // Handle icons
  copyAll( `${ modules }/@cfpb/cfpb-icons/src/icons`, `${ baseConfig.outdir }/icons` );

  // Handle prebuilt lightbox dep
  [
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
    ) ) );
};
