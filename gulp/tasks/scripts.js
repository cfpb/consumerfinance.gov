'use strict';

/* scripts task
   ---------------
   Bundle javascripty things!
   This task is set up to generate multiple separate bundles,
   from different sources, and to use watch when run from the default task.
*/

const browserSync = require( 'browser-sync' );
const gulp = require( 'gulp' );
const gulpConcat = require( 'gulp-concat' );
const gulpModernizr = require( 'gulp-modernizr' );
const gulpRename = require( 'gulp-rename' );
const gulpReplace = require( 'gulp-replace' );
const gulpUglify = require( 'gulp-uglify' );
const handleErrors = require( '../utils/handle-errors' );
const paths = require( '../../config/environment' ).paths;
const webpack = require( 'webpack' );
const webpackConfig = require( '../../config/webpack-config.js' );
const webpackStream = require( 'webpack-stream' );
const configLegacy = require( '../config.js' ).legacy;

/**
 * Standardize webpack workflow for handling script
 * configuration, source, and destination settings.
 * @param {Object} config - Settings for webpack.
 * @param {string} src - Source URL in the unprocessed assets directory.
 * @param {string} dest - Destination URL in the processed assets directory.
 * @returns {PassThrough} A source stream.
 */
function _processScript( config, src, dest ) {
  return gulp.src( paths.unprocessed + src )
    .pipe( webpackStream( config, webpack ) )
    .on( 'error', handleErrors )
    .pipe( gulp.dest( paths.processed + dest ) )
    .pipe( browserSync.reload( {
      stream: true
    } ) );
}

/**
 * Generate modernizr polyfill bundle.
 * @returns {PassThrough} A source stream.
 */
function scriptsPolyfill() {
  return gulp.src( paths.unprocessed + '/js/routes/common.js' )
    .pipe( gulpModernizr( {
      tests:   [ 'csspointerevents', 'classlist', 'es5' ],
      options: [ 'setClasses', 'html5printshiv' ]
    } ) )
    .pipe( gulpUglify( {
      compress: {
        properties: false
      }
    } ) )
    .pipe( gulpRename( 'modernizr.min.js' ) )
    .on( 'error', handleErrors )
    .pipe( gulp.dest( paths.processed + '/js/' ) )
    .pipe( browserSync.reload( {
      stream: true
    } ) );
}

/**
 * Bundle scripts in unprocessed/js/routes/
 * and factor out common modules into common.js.
 * @returns {PassThrough} A source stream.
 */
function scriptsModern() {
  return _processScript( webpackConfig.modernConf,
                         '/js/routes/common.js', '/js/routes/' );
}

/**
 * Bundle IE9-specific script.
 * @returns {PassThrough} A source stream.
 */
function scriptsIE() {
  return _processScript( webpackConfig.ieConf,
                         '/js/ie/common.ie.js', '/js/ie/' );
}

/**
 * Bundle external site scripts.
 * @returns {PassThrough} A source stream.
 */
function scriptsExternal() {
  return _processScript( webpackConfig.externalConf,
                         '/js/routes/external-site/index.js', '/js/' );
}

/**
 * Bundle atomic component scripts.
 * Provides a means to bundle JS for specific atomic components,
 * which then can be carried over to other projects.
 * @returns {PassThrough} A source stream.
 */
function scriptsOnDemand() {
  return _processScript( webpackConfig.onDemandConf,
                         '/js/routes/on-demand/*.js', '/js/atomic/' );
}

 /**
  * Bundle base js for Spanish Ask CFPB pages.
  * @returns {PassThrough} A source stream.
  */
function scriptsSpanish() {
  return _processScript( webpackConfig.spanishConf,
                          '/js/routes/es/obtener-respuestas/single.js', '/js/' );
}

/**
 * Bundle atomic component scripts for non-responsive pages.
 * Provides a means to bundle JS for specific atomic components,
 * which then can be carried over to other projects.
 * @returns {PassThrough} A source stream.
 */
function scriptsNonResponsive() {
  return gulp.src( paths.unprocessed + '/js/routes/on-demand/header.js' )
    .pipe( webpackStream( webpackConfig.onDemandHeaderRawConf, webpack ) )
    .on( 'error', handleErrors )
    .pipe( gulpRename( 'header.nonresponsive.js' ) )
    .pipe( gulpReplace( 'breakpointState.isInDesktop()', 'true' ) )
    .pipe( gulpUglify() )
    .pipe( gulp.dest( paths.processed + '/js/atomic/' ) )
    .pipe( browserSync.reload( {
      stream: true
    } ) );
}

/**
 * Process Nemo JS files.
 * @returns {PassThrough} A source stream.
 */
function scriptsNemo() {
  return gulp.src( configLegacy.scripts )
    .pipe( gulpConcat( 'scripts.js' ) )
    .on( 'error', handleErrors )
    .pipe( gulpUglify() )
    .pipe( gulpRename( 'scripts.min.js' ) )
    .pipe( gulp.dest( configLegacy.dest + '/nemo/_/js' ) )
    .pipe( browserSync.reload( {
      stream: true
    } ) );
}

/**
 * Bundle Es5 shim scripts.
 * @returns {PassThrough} A source stream.
 */
function scriptsEs5Shim() {
  return gulp.src( paths.unprocessed + '/js/shims/es5-shim.js' )
    .pipe( webpackStream( {
      entry: paths.unprocessed + '/js/shims/es5-shim.js',
      output: {
        filename: 'es5-shim.js'
      }
    }, webpack ) )
    .pipe( gulpUglify() )
    .on( 'error', handleErrors )
    .pipe( gulp.dest( paths.processed + '/js/' ) )
    .pipe( browserSync.reload( {
      stream: true
    } ) );
}

gulp.task( 'scripts:polyfill', scriptsPolyfill );
gulp.task( 'scripts:modern', scriptsModern );
gulp.task( 'scripts:ie', scriptsIE );
gulp.task( 'scripts:external', scriptsExternal );
gulp.task( 'scripts:spanish', scriptsSpanish );
gulp.task( 'scripts:ondemand:base', scriptsOnDemand );
gulp.task( 'scripts:ondemand:nonresponsive', scriptsNonResponsive );
gulp.task( 'scripts:ondemand', [
  'scripts:ondemand:base',
  'scripts:ondemand:nonresponsive'
] );
gulp.task( 'scripts:nemo', scriptsNemo );
gulp.task( 'scripts:es5-shim', scriptsEs5Shim );

gulp.task( 'scripts', [
  'scripts:polyfill',
  'scripts:modern',
  'scripts:ie',
  'scripts:external',
  'scripts:nemo',
  'scripts:es5-shim',
  'scripts:spanish'
] );
