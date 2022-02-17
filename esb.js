/* eslint-disable no-sync,max-lines-per-function,global-require */
const { readdirSync } = require( 'fs' );
const { readdir, mkdir, copyFile } = require( 'fs' ).promises;
const { resolve, dirname } = require( 'path' );
const esbuild = require( 'esbuild' );
const postCSSPlugin = require( 'esbuild-plugin-postcss2' );
const autoprefixer = require( 'autoprefixer' );

const cfpbModules = './node_modules/@cfpb';

const unprocessed = './cfgov/unprocessed';
const css = `${ unprocessed }/css`;
const r = `${ unprocessed }/js/routes`;
const a = `${ unprocessed }/apps`;
const od = `${ r }/on-demand`;

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

( async () => {
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

  const jsPaths = [
  // header and footer
    `${ r }/common.js`,

    // js for entire sub-paths
    `${ r }/ask-cfpb/single.js`,
    `${ r }/credit-cards/single.js`,
    `${ r }/es/single.js`,
    `${ r }/external-site/single.js`,
    // js for specific pages, based on url
    `${ r }/about-us/careers/current-openings/index.js`,
    `${ r }/consumer-tools/debt-collection/index.js`,
    `${ r }/data-research/prepaid-accounts/search-agreements/index.js`,
    `${ r }/owning-a-home/mortgage-estimate/index.js`,
    `${ r }/owning-a-home/index.js`,

    // on-demand: components included on a page via Wagtatil
    ...getAll( od ),
    `${ od }/simple-chart/simple-chart.js`,
    `${ od }/youth-employment-programs/buying-a-car/index.js`,
    // apps
    ...getAll( `${ a }/admin/js` ),
    ...getAll( `${ a }/analytics-gtm/js` ),
    `${ a }/ccdb-landing-map/js/index.js`,
    `${ a }/financial-well-being/js/home.js`,
    `${ a }/financial-well-being/js/results.js`,
    `${ a }/find-a-housing-counselor/js/common.js`,
    `${ a }/form-explainer/js/FormExplainer.js`,
    `${ a }/owning-a-home/js/common.js`,
    `${ a }/owning-a-home/js/explore-rates/index.js`,
    `${ a }/owning-a-home/js/mortgage-estimate/index.js`,
    `${ a }/owning-a-home/js/form-explainer/index.js`,
    `${ a }/paying-for-college/js/disclosure-feedback.js`,
    `${ a }/paying-for-college/js/college-costs.js`,
    `${ a }/paying-for-college/js/repay.js`,
    `${ a }/regulations3k/js/index.js`,
    `${ a }/regulations3k/js/permalinks.js`,
    `${ a }/regulations3k/js/recent-notices.js`,
    `${ a }/regulations3k/js/search.js`,
    `${ a }/retirement/js/index.js`,
    `${ a }/rural-or-underserved-tool/js/common.js`,
    `${ a }/teachers-digital-platform/js/index.js`,
    `${ a }/youth-employment-success/js/index.js`
  ];

  const styledApps = [
    'ccdb-landing-map',
    'find-a-housing-counselor',
    'form-explainer',
    'know-before-you-owe',
    'owning-a-home',
    'paying-for-college',
    'prepaid-agreements',
    'regulations3k',
    'retirement',
    'rural-or-underserved-tool',
    'teachers-digital-platform',
    'youth-employment-success'
  ];

  const cssPaths = [
    `${ css }/main.less`,
    `${ css }/header.less`,
    `${ css }/footer.less`,
    ...getAll( `${ css }/on-demand/`, /.less$/ ),
    ...styledApps.map( v => `${ a }/${ v }/css/main.less` )
  ];

  const baseConfig = {
    logLevel: 'info',
    bundle: true,
    minify: true,
    sourcemap: true,
    external: [ '*.png', '*.woff', '*.woff2', '*.gif', '*.svg' ],
    outdir: 'cfgov/static_built/out'
  };

  /*
  const watchConfig = {
    ...baseConfig,
    watch: true
  };
*/

  // Static
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
    './node_modules/lightbox2/dist/css/lightbox.min.css',
    './node_modules/lightbox2/dist/images/close.png',
    './node_modules/lightbox2/dist/images/loading.gif',
    './node_modules/lightbox2/dist/images/next.png',
    './node_modules/lightbox2/dist/images/prev.png',
    './node_modules/lightbox2/dist/js/lightbox-plus-jquery.min.js'
  ].map( f => copyFile(
    f, f.replace(
      'node_modules/lightbox2/dist',
      `${ baseConfig.outdir }/lightbox2`
    ) ) )
  );


  // JS
  esbuild.build( { ...baseConfig, entryPoints: jsPaths } );

  // CSS
  esbuild.build( {
    ...baseConfig,
    entryPoints: cssPaths,
    plugins: [ postCSSPlugin.default( {
      plugins: [ autoprefixer ],
      lessOptions: {
        compress: true,
        math: 'always',
        paths: [
          ...readdirSync( cfpbModules ).map( v => `${ cfpbModules }/${ v }/src` ),
          './node_modules/cfpb-chart-builder/src/css'
        ]
      }
    } ) ]
  } );

  // Run app-specific scripts
  require( './cfgov/unprocessed/apps/regulations3k/worker_and_manifest.js' );
} )();
