'use strict';

var gulp = require( 'gulp' );
var $ = require( 'gulp-load-plugins' )();
var config = require( '../config' ).lint;
var handleErrors = require( '../utils/handleErrors' );


/**
 * Lints all the js files for errors
 */
gulp.task( 'lint', [
  'lint:gulp',
  'lint:src'
] );


/**
 * Lints the gulpfile for errors
 */
gulp.task( 'lint:gulp', function() {
  return gulp.src( config.gulp )
    .pipe( $.eslint() )
    .pipe( $.eslint.format() )
    .on( 'error', handleErrors );
} );


/**
 * Lints the source js files for errors
 */
gulp.task( 'lint:src', function() {
  return gulp.src( config.src )
    .pipe( $.eslint() )
    .pipe( $.eslint.format() )
    .on( 'error', handleErrors );
} );
