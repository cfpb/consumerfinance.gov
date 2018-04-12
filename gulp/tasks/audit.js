const envvars = require( '../../config/environment' ).envvars;
const fancyLog = require( 'fancy-log' );
const fsHelper = require( '../utils/fs-helper' );
const gulp = require( 'gulp' );
const isReachable = require( 'is-reachable' );
const localtunnel = require( 'localtunnel' );
const minimist = require( 'minimist' );
const spawn = require( 'child_process' ).spawn;
const psi = require( 'psi' );

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
      fancyLog( 'WCAG tests exited with code ' + code );
      process.exit( 1 );
    }
    fancyLog( 'WCAG tests done!' );
  } );
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
  fancyLog( 'WCAG tests checking URL: http://' + url );

  return [ '--u=' + url, '--id=' + checkerId ];
}

/**
 * Run PageSpeed Insight tests.
 */
function testPerf() {
  _createPSITunnel()
    .then( _runPSI )
    .catch( err => {
      fancyLog( err );
    } );
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
      return Promise.reject( new Error( url +
        ' is not reachable. Is your local server running?'
      ) );
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
 * Run PageSpeed Insight (PSI) executable.
 * @param {Object} params - url, options, and tunnel for running PSI.
 */
function _runPSI( params ) {
  fancyLog( 'PSI tests checking URL: ' + params.url );
  psi.output( params.url, params.options )
    .then( () => {
      fancyLog( 'PSI tests done!' );
      params.tunnel.close();
    } )
    .catch( err => {
      fancyLog( err.message );
      params.tunnel.close();
      process.exit( 1 );
    } );
}

gulp.task( 'audit:a11y', testA11y );
gulp.task( 'audit:perf', testPerf );
