'use strict';

var configLint = require( '../config' ).lint;
var gulp = require( 'gulp' );
var gulpEslint = require( 'gulp-eslint' );
var handleErrors = require( '../utils/handle-errors' );
var minimist = require( 'minimist' );
var through = require( 'through2' );

/**
 * Generic lint a script source.
 * @param {string} src The path to the source JavaScript.
 * @returns {Object} An output stream from gulp.
 */
function _genericLint( src ) {
  // Grab the --fix flag from the command-line, if available.
  var commandLineParams = minimist( process.argv.slice( 2 ) );
  var willFix = commandLineParams.fix || false;
  return gulp.src( src, { base: './' } )
    .pipe( gulpEslint( { fix: willFix } ) )
    .pipe( gulpEslint.format() )
    .pipe( gulp.dest( './' ) )
    .pipe(through.obj( function( file, enc, cb ) {
      if( commandLineParams.travis ) {
        return gulpEslint.failAfterError( );
      }

      return cb( null, file );
    } ) )
    .on( 'error', handleErrors );
}

/**
 * Lints the gulpfile for errors.
 */
gulp.task( 'lint:build', function() {
  return _genericLint( configLint.build );
} );

/**
 * Lints the test js files for errors.
 */
gulp.task( 'lint:tests', function() {
  return _genericLint( configLint.test );
} );

/**
 * Lints the source js files for errors.
 */
gulp.task( 'lint:scripts', function() {
  return _genericLint( configLint.src );
} );

/**
 * Lints all the js files for errors
 */
gulp.task( 'lint', [
  'lint:build',
  'lint:tests',
  'lint:scripts'
] );
