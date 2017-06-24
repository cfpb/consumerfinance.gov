'use strict';

const configTest = require( '../config' ).test;
const envvars = require( '../../config/environment' ).envvars;
const fsHelper = require( '../utils/fs-helper' );
const gulp = require( 'gulp' );
const gulpCoveralls = require( 'gulp-coveralls' );
const gulpIstanbul = require( 'gulp-istanbul' );
const gulpMocha = require( 'gulp-mocha' );
const gulpUtil = require( 'gulp-util' );
const isReachable = require( 'is-reachable' );
const localtunnel = require( 'localtunnel' );
const minimist = require( 'minimist' );
const spawn = require( 'child_process' ).spawn;
const psi = require( 'psi' );

/**
 * Run Mocha JavaScript unit tests.
 * @param {Function} cb - Callback function to call on completion.
 */
function testUnitScripts( cb ) {
  gulp.src( configTest.src )
    .pipe( gulpIstanbul( {
      includeUntested: false
    } ) )
    .pipe( gulpIstanbul.hookRequire() )
    .on( 'finish', () => {
      gulp.src( configTest.tests + '/unit_tests/**/*.js' )
        .pipe( gulpMocha( {
          reporter: configTest.reporter ? 'spec' : 'nyan'
        } ) )
        .pipe( gulpIstanbul.writeReports( {
          dir: configTest.tests + '/unit_test_coverage'
        } ) )

        /* TODO: we want this but it breaks because we don't have good coverage
        .pipe( gulpIstanbul.enforceThresholds( {
          thresholds: { global: 90 }
        } ) )
        */
        .on( 'end', cb );
    } );
}

/**
 * Run tox Acceptance tests.
 */
function testAcceptanceBrowser() {
  const params = minimist( process.argv.slice( 3 ) ) || {};
  let toxParams = [ '-e' ];

  if ( params.fast ) {
    toxParams.push( 'acceptance-fast' );
  } else {
    toxParams.push( 'acceptance' );
  }

  Object.keys( params ).forEach( key => {
    if ( key !== '_' ) {
      toxParams.push( key + '=' + params[key] );
    }
  } );

  spawn( 'tox', toxParams, { stdio: 'inherit' } )
  .once( 'close', function( code ) {
    if ( code ) {
      gulpUtil.log( 'Tox tests exited with code ' + code );
      process.exit( 1 );
    }
    gulpUtil.log( 'Tox tests done!' );
  } );
}

/**
 * Add a command-line flag to a list of Protractor parameters, if present.
 * @param {Object} protractorParams Parameters to pass to Protractor binary.
 * @param {Object} commandLineParams Parameters passed
 *   to the command-line as flags.
 * @param {string} value Command-line flag name to lookup.
 * @returns {Array} List of Protractor binary parameters as strings.
 */
function _addCommandLineFlag( protractorParams, commandLineParams, value ) {
  if ( typeof commandLineParams[value] === 'undefined' ) {
    return protractorParams;
  }

  if ( value === 'tags' ) {
    return protractorParams.concat( [ '--cucumberOpts.tags' +
                                      '=' +
                                      commandLineParams[value] ] );
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
  const commandLineParams = minimist( process.argv.slice( 2 ) );
  const configFile = commandLineParams.a11y ?
                     'test/browser_tests/a11y_conf.js' :
                     'test/browser_tests/conf.js';

  // Set default configuration command-line parameter.
  let params = [ configFile ];

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

  // If --tags=@tagName flag is added on the command-line.
  params = _addCommandLineFlag( params, commandLineParams, 'tags' );

  // If the --suite=suite1,suite2 flag is added on the command-line
  // or, if not, if a suite is passed as part of the gulp task definition.
  const suiteParam = { suite: commandLineParams.suite || suite };
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
  const commandLineParams = minimist( process.argv.slice( 2 ) );
  const host = envvars.TEST_HTTP_HOST;
  const port = envvars.TEST_HTTP_PORT;
  const checkerId = envvars.ACHECKER_ID;
  const urlPath = _parsePath( commandLineParams.u );
  const url = host + ':' + port + urlPath;
  gulpUtil.log( 'WCAG tests checking URL: http://' + url );

  return [ '--u=' + url, '--id=' + checkerId ];
}

/**
 * Processes command-line and environment variables
 * for passing to the PageSpeed Insights (PSI) executable.
 * An optional URL path comes from the command-line `--u=` flag.
 * A PSI "strategy" (mobile vs desktop) can be specified with the `--s=` flag.
 * @returns {Promise}
 *   Promise containing an array of command-line arguments for PSI binary.
 */
function _createPSITunnel() {
  const commandLineParams = minimist( process.argv.slice( 2 ) );
  const host = envvars.TEST_HTTP_HOST;
  const port = envvars.TEST_HTTP_PORT;
  const path = _parsePath( commandLineParams.u );
  const url = commandLineParams.u || host + ':' + port + path;
  const strategy = commandLineParams.s || 'mobile';

  /**
   * Create local tunnel and pass promise params
   * to callback function.
   * @param {boolean} reachable If port is reachable.
   * @returns {Promise} A promise which calls local tunnel.
   */
  function _createLocalTunnel( reachable ) {
    if ( !reachable ) {
      return Promise.reject( url +
        ' is not reachable. Is your local server running?'
      );
    }

    return new Promise( ( resolve, reject ) => {
      localtunnel( port, _localTunnelCallback.bind( null, resolve, reject ) );
    } );
  }

   /**
   * Local tunnel callback function
   * @param {Function} resolve Promise fulfillment callback.
   * @param {Function} reject Promise rejection callback.
   * @param {Error} err Local tunnel error.
   * @param {Object} tunnel Local tunnel object.
   * @returns {Promise} callback promise.
   */
  function _localTunnelCallback( resolve, reject, err, tunnel ) {
    if ( err ) {
      return reject( 'Error: ' + err.message );
    }

    const fullTunnelUrl = tunnel.url + path;

    return resolve( {
      options: { strategy: strategy },
      tunnel:  tunnel,
      url:     fullTunnelUrl
    } );
  }

  // Check if server is reachable.
  return isReachable( url )
         .then( _createLocalTunnel );
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
  ).once( 'close', code => {
    if ( code ) {
      gulpUtil.log( 'WCAG tests exited with code ' + code );
      process.exit( 1 );
    }
    gulpUtil.log( 'WCAG tests done!' );
  } );
}

/**
 * Run PageSpeed Insight (PSI) executable.
 * @param {Object} params - url, options, and tunnel for running PSI.
 */
function _runPSI( params ) {
  gulpUtil.log( 'PSI tests checking URL: http://' + params.url );
  psi.output( params.url, params.options )
  .then( () => {
    gulpUtil.log( 'PSI tests done!' );
    params.tunnel.close();
  } )
  .catch( err => {
    gulpUtil.log( err.message );
    params.tunnel.close();
    process.exit( 1 );
  } );
}

/**
 * Run PageSpeed Insight tests.
 */
function testPerf() {
  _createPSITunnel()
  .then( _runPSI )
  .catch( err => {
    gulpUtil.log( err );
  } );
}

/**
 * Spawn the appropriate acceptance tests.
 * @param {string} args Selenium arguments.
 */
function spawnProtractor( args ) {
  let UNDEFINED;

  if ( typeof args === 'function' ) {
    args = UNDEFINED;
  }
  const params = _getProtractorParams( args );

  gulpUtil.log( 'Running Protractor with params: ' + params );
  spawn(
    fsHelper.getBinary( 'protractor', 'protractor', '../bin/' ),
    params,
    { stdio: 'inherit' }
  ).once( 'close', code => {
    if ( code ) {
      gulpUtil.log( 'Protractor tests exited with code ' + code );
      process.exit( 1 );
    }
    gulpUtil.log( 'Protractor tests done!' );
  }
  );
}

/**
 * Run coveralls reports on Travis.
 */
function testCoveralls() {
  gulp.src( configTest.tests + '/unit_test_coverage/lcov.info' )
    .pipe( gulpCoveralls() );
}

gulp.task( 'test', [ 'lint', 'test:unit' ] );
gulp.task( 'test:a11y', testA11y );
gulp.task( 'test:acceptance', testAcceptanceBrowser );
gulp.task( 'test:acceptance:protractor', spawnProtractor );
gulp.task( 'test:coveralls', testCoveralls );
gulp.task( 'test:perf', testPerf );
gulp.task( 'test:unit', [ 'test:unit:scripts' ] );
gulp.task( 'test:unit:scripts', testUnitScripts );
