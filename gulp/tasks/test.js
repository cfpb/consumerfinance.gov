const configTest = require( '../config' ).test;
const envvars = require( '../../config/environment' ).envvars;
const fsHelper = require( '../utils/fs-helper' );
const gulp = require( 'gulp' );
const gulpIstanbul = require( 'gulp-istanbul' );
const gulpMocha = require( 'gulp-mocha' );
const gulpUtil = require( 'gulp-util' );
const minimist = require( 'minimist' );
const spawn = require( 'child_process' ).spawn;
const SauceConnectTunnel = require( 'sauce-connect-tunnel' );

/**
 * Run Mocha JavaScript unit tests.
 * @param {Function} cb - Callback function to call on completion.
 */
function testUnitScripts( cb ) {
  const params = minimist( process.argv.slice( 3 ) ) || {};

  /* If --specs=path/to/js/spec flag is added on the command-line,
     pass the value to mocha to test individual unit test files. */
  const specs = params.specs;
  let src = configTest.tests + '/unit_tests/';

  if ( specs ) {
    src += specs;
  } else {
    src += '**/*.js';
  }

  gulp.src( configTest.src )
    .pipe( gulpIstanbul( {
      includeUntested: false
    } ) )
    .pipe( gulpIstanbul.hookRequire() )
    .on( 'finish', () => {
      gulp.src( src )
        .pipe( gulpMocha( {
          reporter: configTest.reporter ? 'spec' : 'nyan'
        } ) )
        .pipe( gulpIstanbul.writeReports( {
          dir: configTest.tests + '/unit_test_coverage'
        } ) )

        /* TODO: we want this but it breaks because we don't have good coverage
           .pipe( gulpIstanbul.enforceThresholds( {
           thresholds: { global: 90 }
           } ) ) */
        .on( 'end', cb );
    } );
}


/**
 * Run tox Acceptance tests.
 */
function testAcceptanceBrowser() {
  const params = minimist( process.argv.slice( 3 ) ) || {};
  const toxParams = [ '-e' ];

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
    const ERROR_MSG = 'Please ensure your SAUCE variables are set.';
    gulpUtil.colors.enabled = true;
    gulpUtil.log( gulpUtil.colors.red( ERROR_MSG ) );

    return Promise.reject( new Error( ERROR_MSG ) );
  }

  return new Promise( ( resolve, reject ) => {
    const sauceTunnel = new SauceConnectTunnel( SAUCE_USERNAME,
      SAUCE_ACCESS_KEY,
      SAUCE_TUNNEL_ID );
    const sauceTunnelParam = { sauceTunnel: sauceTunnel };

    sauceTunnel.on( 'verbose:debug', debugMsg => {
      gulpUtil.log( debugMsg );
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
      }, 5000 );
    } );

  } );
}

/**
 * Spawn the appropriate acceptance tests.
 * @param {string} args Protractor arguments.
 */
function spawnProtractor( ) {
  const params = _getProtractorParams();

  /**
   * Spawn the appropriate acceptance tests.
   * @param {string} args Protractor arguments.
   * @returns {Promise} Promise which runs Protractor.
   */
  function _runProtractor( args ) {
    gulpUtil.log( 'Running Protractor with params: ' + params );

    return new Promise( ( resolve, reject ) => {
      spawn(
        fsHelper.getBinary( 'protractor', 'protractor', '../bin/' ),
        params,
        { stdio: 'inherit' }
      ).once( 'close', code => {
        if ( code ) {
          gulpUtil.log( 'Protractor tests exited with code ' + code );
          reject( args );
        }
        gulpUtil.log( 'Protractor tests done!' );
        resolve( args );
      } );
    } );
  }

  /**
   * Acceptance tests error handler.
   * @param {string} args Failure arguments.
   */
  function _handleErrors( args = {} ) {
    if ( args.sauceTunnel ) {
      args.sauceTunnel.stop( () => {
        process.exit( 1 );
      } );
    } else {
      process.exit( 1 );
    }
  }

  /**
   * Acceptance tests success handler.
   * @param {string} args Success arguments.
   */
  function _handleSuccess( args = {} ) {
    if ( args.sauceTunnel ) {
      args.sauceTunnel.stop( () => {
        process.exit( 0 );
      } );
    } else {
      process.exit( 0 );
    }
  }

  if ( gulpUtil.env.sauce === 'true' ) {
    _createSauceTunnel()
      .then( _runProtractor )
      .then( _handleSuccess )
      .catch( _handleErrors );
  } else {
    _runProtractor()
      .then( _handleSuccess )
      .catch( _handleErrors );
  }
}

gulp.task( 'test', [ 'lint', 'test:unit' ] );
gulp.task( 'test:acceptance', testAcceptanceBrowser );
gulp.task( 'test:acceptance:protractor', spawnProtractor );
gulp.task( 'test:unit', [ 'test:unit:scripts' ] );
gulp.task( 'test:unit:scripts', testUnitScripts );
