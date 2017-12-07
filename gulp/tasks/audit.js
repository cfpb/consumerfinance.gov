'use strict';

const chromeLauncher = require( 'chrome-launcher' );
const envvars = require( '../../config/environment' ).envvars;
const fsHelper = require( '../utils/fs-helper' );
const gulp = require( 'gulp' );
const gulpUtil = require( 'gulp-util' );
const isReachable = require( 'is-reachable' );
const lighthouse = require( 'lighthouse' );
const lighthousePerfConfig =
  require( 'lighthouse/lighthouse-core/config/perf.json' );
const localtunnel = require( 'localtunnel' );
const minimist = require( 'minimist' );
const spawn = require( 'child_process' ).spawn;
const psi = require( 'psi' );

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
 * Run Google Lighthouse performance audits.
 */
function testPerfLighthouse() {
  const flags = {
    chromeFlags: [ '--headless' ],
    logLevel: 'error',
    output: 'json'
  };

  const urlFirst = 'https://consumerfinance.gov';
  const urlSecond = 'http://localhost:8000';

  _launchChromeAndRunLighthouse( urlFirst, flags, lighthousePerfConfig )
    .then( prodResults => {
      _launchChromeAndRunLighthouse( urlSecond, flags, lighthousePerfConfig )
        .then( localResults => {
          gulpUtil.log(
            '\n',
            'Running Google Lighthouse performance audits on production',
            'www.consumerfinance.gov and localhost.\n',
            'Production should always be slower.',
            gulpUtil.colors.red(
              'If localhost is slower something may be wrong!'
            ),
            '\n\n',
            _formatLighthouseReport( localResults, prodResults ) );
        } );
    } );
}

/**
 * Launch headless Chrome and run Google Lighthouse.
 * @param {string} url website URL to run Lighthouse audit against.
 * @param {Object} [flags={}] CLI flags to enable on Lighthouse.
 * @param {[Object]} [config=null] Configuration to pass to Lighthouse.
 * @returns {Promise} Promise returned from Lighthouse instance.
 */
function _launchChromeAndRunLighthouse( url, flags = {}, config = null ) {
  return chromeLauncher.launch( flags ).then( chrome => {
    flags.port = chrome.port;
    return lighthouse( url, flags, config ).then( results =>
      chrome.kill().then( () => results ) );
  } );
}

/**
 * Format the output of two Google Lighthouse reports to compare them
 * to each other.
 * @param {Object} primaryResults JSON of primary results to check.
 * @param {Object} secondaryResults JSON of results to compare to primary.
 * @returns {string} Formatted results for display in the console.
 */
function _formatLighthouseReport( primaryResults, secondaryResults ) {
  let output = '';

  // List of metrics Lighthouse reports on. Some don't make sense to
  // report out to the console so we turn them off by setting them false.
  const displayMetrics = {
    'first-meaningful-paint':      true,
    'speed-index-metric':          true,
    'screenshot-thumbnails':       false,
    'estimated-input-latency':     true,
    'time-to-first-byte':          true,
    'first-interactive':           true,
    'consistently-interactive':    true,
    'user-timings':                false,
    'critical-request-chains':     false,
    'redirects':                   false,
    'mainthread-work-breakdown':   true,
    'bootup-time':                 true,
    'uses-long-cache-ttl':         false,
    'total-byte-weight':           true,
    'offscreen-images':            true,
    'uses-webp-images':            false,
    'uses-optimized-images':       false,
    'uses-request-compression':    false,
    'uses-responsive-images':      true,
    'dom-size':                    true,
    'link-blocking-first-paint':   true,
    'script-blocking-first-paint': true
  };
  const results = primaryResults;
  let currMetric;
  let compMetric = secondaryResults;
  for ( const metric in results.audits ) {
    if ( results.audits.hasOwnProperty( metric ) ) {
      currMetric = results.audits[metric];
      compMetric = secondaryResults.audits[metric];
      if ( displayMetrics[metric] ) {
        output += '\n' +
          currMetric.description + ': \n' +
          gulpUtil.colors.grey( currMetric.helpText.split( '[' )[0] ) + '\n' +
          '  ' + gulpUtil.colors.cyan( currMetric.displayValue +
          ' (localhost)' ) + '\n' +
          '  ' + gulpUtil.colors.green( compMetric.displayValue +
          ' (production)' );

        if ( currMetric.rawValue &&
             currMetric.rawValue > compMetric.rawValue ) {
          output += gulpUtil.colors.red( ' !!!' );
        }
      }
    }
  }

  return output;
}

/**
 * Run PageSpeed Insight tests.
 */
function testPerfPSI() {
  _createPSITunnel()
  .then( _runPSI )
  .catch( err => {
    gulpUtil.log( err );
  } );
}

gulp.task(
  'audit', [ 'audit:a11y', 'audit:perf:psi', 'audit:perf:lighthouse' ]
);
gulp.task( 'audit:a11y', testA11y );
gulp.task( 'audit:perf', [ 'audit:perf:psi' ] );
gulp.task( 'audit:perf:psi', testPerfPSI );
gulp.task( 'audit:perf:lighthouse', testPerfLighthouse );
