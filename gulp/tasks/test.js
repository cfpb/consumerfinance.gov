'use strict';

var gulp = require( 'gulp' );
var $ = require( 'gulp-load-plugins' )();
var sitespeedio = require( 'gulp-sitespeedio' );
var childProcess = require( 'child_process' );
var exec = childProcess.exec;
var spawn = childProcess.spawn;
var config = require( '../config' ).test;
var fsHelper = require( '../utils/fsHelper' );
var minimist = require( 'minimist' );

gulp.task( 'test:unit:scripts', function( cb ) {
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

  return params;
}

/**
 * Processes environment variables to find homepage URL
 * where the site is running.
 * @returns {string} URL of website homepage.
 */

function _getSiteUrl() {
  var host = process.env.HTTP_HOST || 'localhost'; // eslint-disable-line no-process-env, no-inline-comments, max-len
  var port = process.env.HTTP_PORT || '8000'; // eslint-disable-line no-process-env, no-inline-comments, max-len
  return 'http://' + host + ':' + port;
}

gulp.task( 'test:perf', sitespeedio( {
  url: _getSiteUrl(),
  depth: 1,
  html: true,
  resultBaseDir: config.tests + '/perf_test_results/',
  showFailedOnly: true,
  skipTest: 'jsnumreq,' +
            'ycompress,' +
            'ydns,' +
            'yfavicon,' +
            'thirdpartyasyncjs,' +
            'syncjsinhead,' +
            'avoidfont,' +
            'expiresmod,' +
            'longexpirehead,' +
            'textcontent,' +
            'thirdpartyversions,' +
            'ycdn,' +
            'connectionclose,' +
            'ycookiefree,' +
            'yexpressions,' +
            'inlinecsswhenfewrequest,' +
            'nodnslookupswhenfewrequests',
  budget: {
    rules: {
      'default': 90
    }
  }
} ) );

gulp.task( 'test:acceptance:browser', function() {
  spawn(
    fsHelper.getBinary( 'protractor' ),
    _getProtractorParams(),
    { stdio: 'inherit' }
  )
    .once( 'close', function() {
      $.util.log( 'Protractor tests done!' );
    } );
} );

gulp.task( 'test:acceptance',
  [
    'test:acceptance:browser'
  ]
);

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
  var host = process.env.HTTP_HOST || 'localhost'; // eslint-disable-line no-process-env, no-inline-comments, max-len
  var port = process.env.HTTP_PORT || '8000'; // eslint-disable-line no-process-env, no-inline-comments, max-len
  var checkerId = process.env.ACHECKER_ID || ''; // eslint-disable-line no-process-env, no-inline-comments, max-len
  var urlPath = _parsePath( commandLineParams.u );
  var url = host + ':' + port + urlPath;
  $.util.log( 'WCAG tests checking URL: http://' + url );
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

gulp.task( 'test:a11y', function() {
  spawn(
    fsHelper.getBinary( 'wcag', '.bin' ),
    _getWCAGParams(),
    { stdio: 'inherit' }
  )
    .once( 'close', function() {
      $.util.log( 'WCAG tests done!' );
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
    'test:unit:scripts',
    'test:unit:macro'
  ]
);
