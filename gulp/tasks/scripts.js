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

/**
 * Use webpack to bundle JavaScript.
 * @param {boolean} watch Whether to run with the watch flag or not.
 * @returns {Object} Returns a stream from gulp.
 */
function webpackTask( watch ) {
  webpackConfig.watch = watch || false;

  return gulp.src( './src/static/js/routes/common.js' )
    .pipe( webpackStream( webpackConfig ) )
    .on( 'error', handleErrors )
    .pipe( gulp.dest( './dist/static/js/routes/' ) )
    .pipe( browserSync.reload( {
      stream: true
    } ) );
}

gulp.task( 'scripts', function() {
  return webpackTask();
} );

// Exporting the task so we can call it directly in our watch task,
// with the 'watch' option.
module.exports = {
  webpackTask: webpackTask
};
