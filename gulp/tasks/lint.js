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
  // Pass all command line flags to EsLint.
  const options = minimist( process.argv.slice( 2 ) );
  let errorHandler = through2.obj();

  if ( options.ci ) {
    options.quiet = true;
    errorHandler = gulpEslint.failAfterError();
  }

  return gulp.src( src, { base: './' } )
    .pipe( gulpEslint( options ) )
    .pipe( gulpEslint.format() )
    .pipe( errorHandler )
    .pipe( gulp.dest( './' ) )
    .on( 'error', handleErrors );
}

/**
 * Lints the gulpfile for errors.
 */
gulp.task( 'lint:build', () => _genericLint( configLint.build ) );

/**
 * Lints the test js files for errors.
 */
gulp.task( 'lint:tests', () => _genericLint( configLint.test ) );

/**
 * Lints the source js files for errors.
 */
gulp.task( 'lint:scripts', () => _genericLint( configLint.src ) );

/**
 * Lints all the js files for errors
 */
gulp.task( 'lint',

  /* Checks to see if a flag for a specific file is present, if so, use it
     Else, returns a list of sane default tasks to run */
  ( () => {
    let UNDEFINED;
    const argv = minimist( process.argv.slice( 3 ) );
    if ( argv.path !== UNDEFINED ) {
      return gulp.parallel( () => _genericLint( argv.path ) );
    }
    return gulp.parallel(
      'lint:build',
      'lint:tests',
      'lint:scripts'
    );
  } )()
);
