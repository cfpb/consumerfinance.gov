'use strict';

/* scripts task
   ---------------
   Bundle javascripty things!
   This task is set up to generate multiple separate bundles, from
   different sources, and to use watch when run from the default task.
*/

var gulp = require( 'gulp' );
var browserSync = require( 'browser-sync' );
var handleErrors = require( '../utils/handleErrors' );
var webpackConfig = require( '../../config/webpack-config.js' );
var webpackStream = require( 'webpack-stream' );
var paths = require( '../../config/environment' ).paths;

gulp.task( 'scripts', ['buildScriptsRoutes'], function() {
  return gulp.src( paths.unprocessed + '/js/routes/common.js' )
    .pipe( webpackStream( webpackConfig ) )
    .on( 'error', handleErrors )
    .pipe( gulp.dest( paths.processed + '/js/routes/' ) )
    .pipe( browserSync.reload( {
      stream: true
    } ) );
} );
