'use strict';

var gulp = require( 'gulp' );
var $ = require( 'gulp-load-plugins' )();
var config = require( '../config' ).lint;
var handleErrors = require( '../utils/handleErrors' );

/**
 * Generic lint a script source.
 * @param {string} src The path to the source JavaScript.
 * @returns {Object} An output stream from gulp.
 */
function _genericLint( src ) {
  return gulp.src( src )
    .pipe( $.eslint() )
    .pipe( $.eslint.format() )
    .on( 'error', handleErrors );
}

/**
 * Lints the gulpfile for errors.
 */
gulp.task( 'lint:build', function() {
  return _genericLint( config.build );
} );

/**
 * Lints the test js files for errors.
 */
gulp.task( 'lint:tests', function() {
  return _genericLint( config.test );
} );

/**
 * Lints the source js files for errors.
 */
gulp.task( 'lint:scripts', function() {
  return _genericLint( config.src );
} );

/**
 * Lints all the js files for errors
 */
gulp.task( 'lint', [
  'lint:build',
  'lint:tests',
  'lint:scripts'
] );
