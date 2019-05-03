/* scripts task
   ---------------
   Bundle javascripty things!
   This task is set up to generate multiple separate bundles,
   from different sources, and to use watch when run from the default task. */

const config = require( '../config.js' );
const configLegacy = config.legacy;
const configScripts = config.scripts;
const fs = require( 'fs' );
const gulp = require( 'gulp' );
const gulpConcat = require( 'gulp-concat' );
const gulpModernizr = require( 'gulp-modernizr' );
const gulpNewer = require( 'gulp-newer' );
const gulpRename = require( 'gulp-rename' );
const gulpReplace = require( 'gulp-replace' );
const gulpTerser = require( 'gulp-terser' );
const handleErrors = require( '../utils/handle-errors' );
const vinylNamed = require( 'vinyl-named' );
const mergeStream = require( 'merge-stream' );
const paths = require( '../../config/environment' ).paths;
const path = require( 'path' );
const webpack = require( 'webpack' );
const webpackConfig = require( '../../config/webpack-config.js' );
const webpackStream = require( 'webpack-stream' );

/**
 * Standardize webpack workflow for handling script
 * configuration, source, and destination settings.
 * @param {Object} localWebpackConfig - Settings for Webpack.
 * @param {string} src - Source URL in the unprocessed assets directory.
 * @param {string} dest - Destination URL in the processed assets directory.
 * @returns {PassThrough} A source stream.
 */
function _processScript( localWebpackConfig, src, dest ) {
  return gulp.src( paths.unprocessed + src )
    .pipe( gulpNewer( {
      dest:  paths.processed + dest,
      extra: configScripts.otherBuildTriggerFiles
    } ) )
    .pipe( vinylNamed( file => file.relative ) )
    .pipe( webpackStream( localWebpackConfig, webpack ) )
    .on( 'error', handleErrors.bind( this, { exitProcess: true } ) )
    .pipe( gulp.dest( paths.processed + dest ) );
}

/**
 * Generate modernizr polyfill bundle.
 * @returns {PassThrough} A source stream.
 */
function scriptsPolyfill() {
  return gulp.src( paths.unprocessed + '/js/routes/common.js' )
    .pipe( gulpNewer( {
      dest:  paths.processed + '/js/modernizr.min.js',
      extra: configScripts.otherBuildTriggerFiles
    } ) )

    /* csspointerevents is used by select menu in Capital Framework for IE10.
       es5 is used for ECMAScript 5 feature detection to change js CSS to no-js.
       setClasses sets detection checks as feat/no-feat CSS in html element.
       html5printshiv enables use of HTML5 sectioning elements in IE8
       See https://github.com/aFarkas/html5shiv */
    .pipe( gulpModernizr( 'modernizr.min.js', {
      options: [ 'setClasses', 'html5printshiv' ],
      tests: [ 'csspointerevents', 'es5' ]
    } ) )
    .pipe( gulpTerser( {
      compress: {
        properties: false
      }
    } ) )
    .on( 'error', handleErrors )
    .pipe( gulp.dest( paths.processed + '/js/' ) );
}

/**
 * Bundle scripts in unprocessed/js/routes/
 * and factor out common modules into common.js.
 * @returns {PassThrough} A source stream.
 */
function scriptsModern() {
  return _processScript(
    webpackConfig.modernConf,
    '/js/routes/**/*.js',
    '/js/routes/'
  );
}

/**
 * Bundle external site scripts.
 * @returns {PassThrough} A source stream.
 */
function scriptsExternal() {
  return _processScript(
    webpackConfig.externalConf,
    '/js/routes/external-site/index.js',
    '/js/'
  );
}

/**
 * Bundle atomic header component scripts.
 * Provides a means to bundle JS for specific atomic components,
 * which then can be carried over to other projects.
 * @returns {PassThrough} A source stream.
 */
function scriptsOnDemandHeader() {
  return _processScript(
    webpackConfig.commonConf,
    '/js/routes/on-demand/header.js',
    '/js/atomic/'
  );
}

/**
 * Bundle atomic header component scripts.
 * Provides a means to bundle JS for specific atomic components,
 * which then can be carried over to other projects.
 * @returns {PassThrough} A source stream.
 */
function scriptsOnDemandFooter() {
  return _processScript(
    webpackConfig.commonConf,
    '/js/routes/on-demand/footer.js',
    '/js/atomic/'
  );
}

/**
 * Bundle atomic component scripts for non-responsive pages.
 * Provides a means to bundle JS for specific atomic components,
 * which then can be carried over to other projects.
 * @returns {PassThrough} A source stream.
 */
function scriptsNonResponsive() {
  return gulp.src( paths.unprocessed + '/js/routes/on-demand/header.js' )
    .pipe( gulpNewer( {
      dest:  paths.processed + '/js/atomic/header.nonresponsive.js',
      extra: configScripts.otherBuildTriggerFiles
    } ) )
    .pipe( webpackStream( webpackConfig.onDemandHeaderRawConf, webpack ) )
    .on( 'error', handleErrors )
    .pipe( gulpRename( 'header.nonresponsive.js' ) )
    .pipe( gulpReplace( 'breakpointState.isInDesktop()', 'true' ) )
    .pipe( gulp.dest( paths.processed + '/js/atomic/' ) );
}

/**
 * Process Nemo JS files.
 * @returns {PassThrough} A source stream.
 */
function scriptsNemo() {
  return gulp.src( configLegacy.scripts )
    .pipe( gulpNewer( {
      dest:  configLegacy.dest + '/nemo/_/js/scripts.min.js',
      extra: configScripts.otherBuildTriggerFiles
    } ) )
    .pipe( gulpConcat( 'scripts.js' ) )
    .on( 'error', handleErrors )
    .pipe( gulpTerser() )
    .pipe( gulpRename( 'scripts.min.js' ) )
    .pipe( gulp.dest( configLegacy.dest + '/nemo/_/js' ) );
}

/**
 * Bundle scripts in /apps/ & factor out shared modules into common.js for each.
 * @returns {PassThrough} A source stream.
 */
function scriptsApps() {
  // Aggregate application namespaces that appear in unprocessed/apps.
  // eslint-disable-next-line no-sync
  let apps = fs.readdirSync( `${ paths.unprocessed }/apps/` );

  // Filter out hidden directories.
  apps = apps.filter( dir => dir.charAt( 0 ) !== '.' );

  // Run each application's JS through webpack and store the gulp streams.
  const streams = [];
  apps.forEach( app => {
    /* Check if node_modules directory exists in a particular app's folder.
       If it doesn't, don't process the scripts and log the command to run. */
    const appsPath = `${ paths.unprocessed }/apps/${ app }`;

    /* Check if webpack-config file exists in a particular app's folder.
       If it exists use it, if it doesn't then use the default config. */
    let appWebpackConfig = webpackConfig.appsConf;
    const appWebpackConfigPath = `${ appsPath }/webpack-config.js`;

    // eslint-disable-next-line no-sync
    if ( fs.existsSync( appWebpackConfigPath ) ) {
      // eslint-disable-next-line global-require
      appWebpackConfig = require( path.resolve( appWebpackConfigPath ) ).conf;
    }

    // eslint-disable-next-line no-sync
    if ( fs.existsSync( `${ appsPath }/package.json` ) ) {
      // eslint-disable-next-line no-sync
      if ( fs.existsSync( `${ appsPath }/node_modules` ) ) {
        streams.push(
          _processScript(
            appWebpackConfig,
            `/apps/${ app }/js/**/*.js`,
            `/apps/${ app }/js`
          )
        );
      } else {
        // eslint-disable-next-line no-console
        console.log(
          '\x1b[31m%s\x1b[0m',
          'App dependencies not installed, please run from project root:',
          `npm --prefix ${ appsPath } install ${ appsPath }`
        );
      }
    }
  } );

  // Return all app's gulp streams as a merged stream.
  let singleStream;

  if ( streams.length > 0 ) {
    singleStream = mergeStream( ...streams );
  } else {
    singleStream = mergeStream();
  }
  return singleStream;
}

gulp.task( 'scripts:apps', scriptsApps );
gulp.task( 'scripts:external', scriptsExternal );
gulp.task( 'scripts:modern', scriptsModern );
gulp.task( 'scripts:nemo', scriptsNemo );
gulp.task( 'scripts:polyfill', scriptsPolyfill );

gulp.task( 'scripts:ondemand:header', scriptsOnDemandHeader );
gulp.task( 'scripts:ondemand:footer', scriptsOnDemandFooter );
gulp.task( 'scripts:ondemand:nonresponsive', scriptsNonResponsive );
gulp.task( 'scripts:ondemand',
  gulp.parallel(
    'scripts:ondemand:header',
    'scripts:ondemand:footer',
    'scripts:ondemand:nonresponsive'
  )
);

gulp.task( 'scripts',
  gulp.parallel(
    'scripts:polyfill',
    'scripts:modern',
    'scripts:apps',
    'scripts:external',
    'scripts:nemo',
    'scripts:ondemand'
  )
);
