const environment = require( '../../config/environment' );
const envvars = environment.envvars;
const fancyLog = require( 'fancy-log' );
const fsHelper = require( '../utils/fs-helper' );
const gulp = require( 'gulp' );
const minimist = require( 'minimist' );
const spawn = require( 'child_process' ).spawn;
const SauceConnectTunnel = require( 'sauce-connect-tunnel' );

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
  let UNDEFINED;
  const commandLineParams = minimist( process.argv.slice( 2 ) );
  const configFile = commandLineParams.a11y ?
    'test/browser_tests/a11y_conf.js' :
    'test/browser_tests/conf.js';

  if ( typeof suite === 'function' ) {
    suite = UNDEFINED;
  }

  // Set default configuration command-line parameter.
  let params = [ configFile ];

  // If --sauce=false flag is added on the command-line.
  params = _addCommandLineFlag( params, commandLineParams, 'sauce' );

  /* If --specs=path/to/js flag is added on the command-line,
     pass the value to protractor to override the default specs to run. */
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

  // If --headless=false flag is added on the command-line.
  params = _addCommandLineFlag( params, commandLineParams, 'headless' );

  /* If the --suite=suite1,suite2 flag is added on the command-line
     or, if not, if a suite is passed as part of the gulp task definition. */
  const suiteParam = { suite: commandLineParams.suite || suite };
  params = _addCommandLineFlag( params, suiteParam, 'suite' );

  return params;
}

/**
 * Create Sauce Labs tunnel.
 * @returns {Promise} Promise which creates Sauce Labs tunnel.
 */
function _createSauceTunnel( ) {
  const SAUCE_USERNAME = envvars.SAUCE_USERNAME;
  const SAUCE_ACCESS_KEY = envvars.SAUCE_ACCESS_KEY;
  const SAUCE_TUNNEL_ID = envvars.SAUCE_TUNNEL;

  if ( !( SAUCE_USERNAME && SAUCE_ACCESS_KEY && SAUCE_TUNNEL_ID ) ) {
    const RED_COLOR = '\x1b[31m%s\x1b[0m';
    const ERROR_MSG = 'Please ensure your SAUCE variables are set.';
    fancyLog( RED_COLOR, ERROR_MSG );
    return Promise.reject( new Error( ERROR_MSG ) );
  }

  return new Promise( ( resolve, reject ) => {
    const sauceTunnel = new SauceConnectTunnel( SAUCE_USERNAME,
      SAUCE_ACCESS_KEY,
      SAUCE_TUNNEL_ID );
    const sauceTunnelParam = { sauceTunnel: sauceTunnel };

    sauceTunnel.on( 'verbose:debug', debugMsg => {
      fancyLog( debugMsg );
    } );

    sauceTunnel.start( status => {
      if ( status === false ) {
        reject( sauceTunnelParam );
      }

      if ( sauceTunnel.proc ) {
        sauceTunnel.proc.on( 'exit', function() {
          reject( sauceTunnelParam );
        } );
      }

      setTimeout( () => {
        resolve( sauceTunnelParam );
      }, 1000 );
    } );

  } );
}

/**
 * Spawn the appropriate acceptance tests.
 * @param {Function} cb - Callback function to call on completion.
 */
async function spawnProtractor( cb ) {
  const params = _getProtractorParams();
  const commandLineParams = minimist( process.argv.slice( 2 ) ) || {};
  let sauceTunnel;

  /**
   * Spawn the appropriate acceptance tests.
   * @returns {Promise} Promise which runs Protractor.
   */
  function _runProtractor( ) {
    fancyLog( 'Running Protractor with params: ' + params );

    return new Promise( ( resolve, reject ) => {
      spawn(
        fsHelper.getBinary( 'protractor', 'protractor', '../bin/' ),
        params,
        { stdio: 'inherit' }
      ).once( 'close', code => {
        if ( code ) {
          reject( new Error( 'Protractor tests exited with code ' + code ) );
        }
        fancyLog( 'Protractor tests done!' );
        resolve();
      } );
    } );
  }

  /**
   * Acceptance tests error handler.
   * @param {Object} args Failure arguments.
   */
  async function _handleErrors( args = {} ) {
    const stopSauceTunnel = () => new Promise( resolve => {
      args.sauceTunnel.stop( resolve );
    } );

    if ( args.sauceTunnel ) {
      await stopSauceTunnel();
    }

    cb(); // eslint-disable-line callback-return
    process.exit( 1 );
  }

  /**
   * Acceptance tests success handler.
   * @param {Object} args Success arguments.
   */
  async function _handleSuccess( args = {} ) {
    const stopSauceTunnel = () => new Promise( resolve => {
      args.sauceTunnel.stop( resolve );
    } );

    if ( args.sauceTunnel ) {
      await stopSauceTunnel();
    }
    cb(); // eslint-disable-line callback-return
    process.exit( 0 );
  }

  try {
    if ( commandLineParams.sauce === 'true' ) {
      sauceTunnel = await _createSauceTunnel();
    }
    await _runProtractor( );
    await _handleSuccess( sauceTunnel );
  } catch ( error ) {
    await _handleErrors( sauceTunnel );
  }
}

gulp.task( 'test:acceptance', spawnProtractor );
