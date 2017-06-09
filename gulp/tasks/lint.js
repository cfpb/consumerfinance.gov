'use strict';

const configLint = require( '../config' ).lint;
const gulp = require( 'gulp' );
const gulpEslint = require( 'gulp-eslint' );
const handleErrors = require( '../utils/handle-errors' );
const minimist = require( 'minimist' );
const through2 = require( 'through2' );

/**
 * Generic lint a script source.
 * @param {string} src The path to the source JavaScript.
 * @returns {Object} An output stream from gulp.
 */
function _genericLint( src ) {
  // Grab the --fix flag from the command-line, if available.
  const commandLineParams = minimist( process.argv.slice( 2 ) );
  const willFix = commandLineParams.fix || false;

  return gulp.src( src, { base: './' } )
    .pipe( gulpEslint( { fix: willFix } ) )
    .pipe( gulpEslint.format() )
    .pipe( ( () => {
      if ( commandLineParams.travis ) {
        return gulpEslint.failAfterError();
      }

      return through2.obj();
    } )( ) )
    .pipe( gulp.dest( './' ) )
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
