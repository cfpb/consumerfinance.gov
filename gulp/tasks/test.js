'use strict';

var envvars = require( '../../config/environment' ).envvars;
var gulp = require( 'gulp' );
var plugins = require( 'gulp-load-plugins' )();
var spawn = require( 'child_process' ).spawn;
var configTest = require( '../config' ).test;
var fsHelper = require( '../utils/fs-helper' );
var minimist = require( 'minimist' );

/**
 * Run Mocha JavaScript unit tests.
 * @param {Function} cb - Callback function to call on completion.
 */
function testUnitScripts( cb ) {
  gulp.src( configTest.src )
    .pipe( plugins.istanbul( {
      includeUntested: false
    } ) )
    .pipe( plugins.istanbul.hookRequire() )
    .on( 'finish', function() {
      gulp.src( configTest.tests + '/unit_tests/**/*.js' )
        .pipe( plugins.mocha( {
          reporter: configTest.reporter ? 'spec' : 'nyan'
        } ) )
        .pipe( plugins.istanbul.writeReports( {
          dir: configTest.tests + '/unit_test_coverage'
        } ) )

        /* TODO: we want this but it breaks because we don't have good coverage
        .pipe( plugins.istanbul.enforceThresholds( {
          thresholds: { global: 90 }
        } ) )
        */

        .on( 'end', cb );
    } );
}

/**
 * Run tox unit tests.
 */
function testUnitServer() {
  spawn(
    'tox',
    { stdio: 'inherit' }
  ).once( 'close', function( code ) {
    if ( code ) {
      plugins.util.log( 'Tox tests exited with code ' + code );
      process.exit( 1 );
    }
    plugins.util.log( 'Tox tests done!' );
  } );
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
 * @param {string} suite Name of specific suite or suites to run, if any.
 * @returns {Array} List of Protractor binary parameters as strings.
 */
function _getProtractorParams( suite ) {

  var commandLineParams = minimist( process.argv.slice( 2 ) );

  var configFile = commandLineParams.a11y ? 'test/browser_tests/a11y_conf.js' : 'test/browser_tests/conf.js';

  // Set default configuration command-line parameter.
  var params = [ configFile ];

  // If --sauce=false flag is added on the command-line.
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

  // If the --suite=suite1,suite2 flag is added on the command-line
  // or, if not, if a suite is passed as part of the gulp task definition.
  var suiteParam = { suite: commandLineParams.suite || suite };
  params = _addCommandLineFlag( params, suiteParam, 'suite' );

  return params;
}

/**
 * Processes command-line and environment variables
 * for passing to the wcag executable.
 * The URL host, port, and AChecker web API ID come from
 * environment variables, while the URL path comes
 * from the command-line `--u=` flag.
 * @returns {Array} Array of command-line arguments for wcag binary.
 */
function _getWCAGParams() {
  var commandLineParams = minimist( process.argv.slice( 2 ) );
  var host = envvars.TEST_HTTP_HOST;
  var port = envvars.TEST_HTTP_PORT;
  var checkerId = envvars.ACHECKER_ID;
  var urlPath = _parsePath( commandLineParams.u );
  var url = host + ':' + port + urlPath;
  plugins.util.log( 'WCAG tests checking URL: http://' + url );

  return [ '--u=' + url, '--id=' + checkerId ];
}

/**
 * Process a path and set it to an empty string if it's undefined
 * and add a leading slash if one is not present.
 * @param {string} urlPath The unprocessed path.
 * @returns {string} The processed path.
 */
function _parsePath( urlPath ) {
  urlPath = urlPath || '';
  if ( urlPath.charAt( 0 ) !== '/' ) {
    urlPath = '/' + urlPath;
  }

  return urlPath;
}

/**
 * Run WCAG accessibility tests.
 */
function testA11y() {
  spawn(
    fsHelper.getBinary( 'wcag', 'wcag', '../.bin' ),
    _getWCAGParams(),
    { stdio: 'inherit' }
  ).once( 'close', function( code ) {
    if ( code ) {
      plugins.util.log( 'WCAG tests exited with code ' + code );
      process.exit( 1 );
    }
    plugins.util.log( 'WCAG tests done!' );
  } );
}

/**
 * Spawn the appropriate acceptance tests.
 * @param {string} suite Name of specific suite or suites to run, if any.
 */
function _spawnProtractor( suite ) {
  var params = _getProtractorParams( suite );
  plugins.util.log( 'Running Protractor with params: ' + params );
  spawn(
    fsHelper.getBinary( 'protractor', 'protractor', '../bin/' ),
    params,
    { stdio: 'inherit' }
  ).once( 'close', function( code ) {
    if ( code ) {
      plugins.util.log( 'Protractor tests exited with code ' + code );
      process.exit( 1 );
    }
    plugins.util.log( 'Protractor tests done!' );
  } );
}

/**
 * Run the protractor acceptance tests.
 * @param {string} suite Name of specific suite or suites to run, if any.
 */
function testAcceptanceBrowser( suite ) {
  _spawnProtractor( suite );
}

/**
 * Run coveralls reports on Travis.
 */
function testCoveralls() {
  gulp.src( configTest.tests + '/unit_test_coverage/lcov.info' )
    .pipe( plugins.coveralls() );
}

// This task will only run on Travis
gulp.task( 'test:coveralls', testCoveralls );

gulp.task( 'test:a11y', testA11y );


gulp.task( 'test:unit:scripts', testUnitScripts );
gulp.task( 'test:unit:server', testUnitServer );

gulp.task( 'test:unit',
  [
    'test:unit:scripts',
    'test:unit:server'
  ]
);

gulp.task( 'test',
  [
    'lint',
    'test:unit'
  ]
);

gulp.task( 'test:acceptance', function() {
  testAcceptanceBrowser();
} );
