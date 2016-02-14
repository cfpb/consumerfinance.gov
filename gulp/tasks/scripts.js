'use strict';

/* scripts task
   ---------------
   Bundle javascripty things!
   This task is set up to generate multiple separate bundles,
   from different sources, and to use watch when run from the default task.
*/

var browserSync = require( 'browser-sync' );
var gulp = require( 'gulp' );
var gulpModernizr = require( 'gulp-modernizr' );
var gulpRename = require( 'gulp-rename' );
var gulpUglify = require( 'gulp-uglify' );
var handleErrors = require( '../utils/handleErrors' );
var paths = require( '../../config/environment' ).paths;
var webpackConfig = require( '../../config/webpack-config.js' );
var webpackStream = require( 'webpack-stream' );

gulp.task( 'scripts', function() {
  return gulp.src( paths.unprocessed + '/js/routes/common.js' )
    .pipe( gulpModernizr( {
      tests:   [ 'csspointerevents', 'classlist' ],
      options: [ 'setClasses',
                 'html5printshiv',
                 'fnBind' ]
    } ) )
    .pipe( gulpUglify() )
    .pipe( gulpRename( 'modernizr.min.js' ) )
    .pipe( gulp.dest( paths.processed + '/js/' ) )
    .pipe( webpackStream( webpackConfig ) )
    .on( 'error', handleErrors )
    .pipe( gulp.dest( paths.processed + '/js/routes/' ) )
    .pipe( browserSync.reload( {
      stream: true
    } ) );
} );
