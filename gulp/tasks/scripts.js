/* scripts task
   ---------------
   Bundle javascripty things!
   This task is set up to generate multiple separate bundles,
   from different sources, and to use watch when run from the default task. */

const config = require( '../config.js' );
const configScripts = config.scripts;
const fs = require( 'fs' );
const gulp = require( 'gulp' );
const gulpNewer = require( 'gulp-newer' );
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
      dest: paths.processed + dest,
      extra: configScripts.otherBuildTriggerFiles
    } ) )
    .pipe( vinylNamed( file => file.relative ) )

    /**
     * @todo ideally after webpack completed building, we would reset
     *       scriptsAppsFilter to '', but leaving it doesn't break anything.
     */
    .pipe( webpackStream( localWebpackConfig, webpack ) )
    .on( 'error', handleErrors.bind( this, { exitProcess: true } ) )
    .pipe( gulp.dest( paths.processed + dest ) );
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

let scriptsAppsFilter = '';

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
    // Allow building just one app
    if ( scriptsAppsFilter && app !== scriptsAppsFilter ) {
      return;
    }

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
      streams.push(
        _processScript(
          appWebpackConfig,
          `/apps/${ app }/js/**/*.js`,
          `/apps/${ app }/js`
        )
      );
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
gulp.task( 'scripts:modern', scriptsModern );

gulp.task( 'scripts:ondemand:header', scriptsOnDemandHeader );
gulp.task( 'scripts:ondemand:footer', scriptsOnDemandFooter );

gulp.task( 'scripts:ondemand',
  gulp.parallel(
    'scripts:ondemand:header',
    'scripts:ondemand:footer'
  )
);

gulp.task( 'scripts',
  gulp.parallel(
    'scripts:modern',
    'scripts:apps',
    'scripts:ondemand',
    'scripts:external'
  )
);

/**
 * If Chokidar gives us an app path, set up filtering in scriptsApp() so
 * only that app is rebuilt.
 *
 * @param {string} chokidarPath Path given by Chokidar file watcher
 */
function setScriptsAppFilter( chokidarPath ) {
  const base = ( paths.unprocessed + '/apps/' ).replace( /^\.\//, '' );
  let appName = '';
  if ( chokidarPath.indexOf( base ) === 0 ) {
    [ appName ] = chokidarPath.substr( base.length ).split( '/' );
  }

  if ( appName ) {
    console.log( `Limiting scripts:apps builds to: ${ appName }` );
    scriptsAppsFilter = appName;
  }
}

gulp.task( 'scripts:watch', function() {
  gulp.watch(
    configScripts.src,
    gulp.parallel( 'scripts:modern' )
  );

  const watcher = gulp.watch(
    paths.unprocessed + '/apps/**/js/**/*.js',
    { delay: 500 },
    gulp.parallel( 'scripts:apps' )
  );
  // We'll just rebuild the app modified
  watcher.on( 'add', setScriptsAppFilter );
  watcher.on( 'change', setScriptsAppFilter );
  watcher.on( 'delete', setScriptsAppFilter );
} );
