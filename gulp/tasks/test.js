'use strict';

var gulp = require( 'gulp' );
var $ = require( 'gulp-load-plugins' )();
var childProcess = require( 'child_process' );
var exec = childProcess.exec;
var spawn = childProcess.spawn;
var config = require( '../config' ).test;
var minimist = require( 'minimist' );
var path = require( 'path' );

gulp.task( 'test:unit:js', function( cb ) {
  gulp.src( config.src )
    .pipe( $.istanbul( {
      includeUntested: true
    } ) )
    .pipe( $.istanbul.hookRequire() )
    .on( 'finish', function() {
      gulp.src( config.tests + '/unit_tests/**/*.js' )
        .pipe( $.mocha( {
          reporter: 'nyan'
        } ) )
        .pipe( $.istanbul.writeReports( {
          dir: config.tests + '/unit_test_coverage'
        } ) )

        /* TODO: we want this but it breaks because we don't have good coverage
        .pipe( $.istanbul.enforceThresholds( {
          thresholds: { global: 90 }
        } ) )
        */

        .on( 'end', cb );
    } );
} );

gulp.task( 'test:unit:macro', function( cb ) {
  exec( 'python ' + config.tests + '/macro_tests/test_macros.py',
    function( err, stdout, stderr ) {
      $.util.log( stdout );
      $.util.log( stderr );
      cb( err );
    }
  );
} );

/**
 * Retrieve a reference path to a binary.
 * @param {string} binaryName The name of the binary to retrieve.
 * @returns {string} Path to the binary to run.
 */
function _getBinary( binaryName ) {
  var winExt = ( /^win/ ).test( process.platform ) ? '.cmd' : '';
  var pkgPath = require.resolve( 'protractor' );
  var protractorDir = path.resolve(
    path.join( path.dirname( pkgPath ), '..', 'bin' )
  );
  return path.join( protractorDir, '/' + binaryName + winExt );
}

/**
 * Add a command-line flag to a list of Protractor parameters, if present.
 * @param {object} protractorParams Parameters to pass to Protractor binary.
 * @param {object} commandLineParams Parameters passed
 *   to the command-line as flags.
 * @param {string} value Command-line flag name to lookup.
 * @returns {Array} List of Protractor binary parameters as strings.
 */
function _addCommandLineFlag( protractorParams, commandLineParams, value ) {
  if ( typeof commandLineParams[value] === 'undefined' ) {
    return protractorParams;
  }
  return protractorParams.concat( [ '--params.' +
                                    value + '=' +
                                    commandLineParams[value] ] );
}

/**
 * Format and return parameters for Protractor binary.
 * @returns {Array} List of Protractor binary parameters as strings.
 */
function _getProtractorParams() {

  // Set default configuration command-line parameter.
  var params = [ 'test/browser_tests/conf.js' ];
  var commandLineParams = minimist( process.argv.slice( 2 ) );

  // If --specs=path/to/js flag is added on the command-line,
  // pass the value to protractor to override the default specs to run.
  params = _addCommandLineFlag( params, commandLineParams, 'sauce' );

  // If --specs=path/to/js flag is added on the command-line,
  // pass the value to protractor to override the default specs to run.
  params = _addCommandLineFlag( params, commandLineParams, 'specs' );

  // If --windowSize=w,h flag is added on the command-line.
  params = _addCommandLineFlag( params, commandLineParams, 'windowSize' );

  // If --browserName=browser flag is added on the command-line.
  params = _addCommandLineFlag( params, commandLineParams, 'browserName' );

  // If --platform=os flag is added on the command-line.
  params = _addCommandLineFlag( params, commandLineParams, 'platform' );

  // If --version=number flag is added on the command-line.
  params = _addCommandLineFlag( params, commandLineParams, 'version' );

  return params;
}

gulp.task( 'test:acceptance:browser', function() {
  spawn(
    _getBinary( 'protractor' ),
    _getProtractorParams(),
    { stdio: 'inherit' } )
      .once( 'close', function() {
        $.util.log( 'Protractor tests done!' );
      } );
} );

// This task will only run on Travis
gulp.task( 'test:coveralls', function() {
  gulp.src( config.tests + '/unit_test_coverage/lcov.info' )
    .pipe( $.coveralls() );
} );

gulp.task( 'test',
  [
    'lint',
    'test:unit',
    'test:acceptance'
  ]
);

gulp.task( 'test:unit',
  [
    'test:unit:js',
    'test:unit:macro'
  ]
);

gulp.task( 'test:acceptance',
  [
    'test:acceptance:browser'
  ]
);
