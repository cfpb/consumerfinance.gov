const environmentTest = require( './environment-test' );
const envvars = require( '../../config/environment' ).envvars;
const defaultSuites = require( './default-suites.js' );
const minimist = require( 'minimist' );
const retry = require( 'protractor-retry' ).retry;

/**
 * Check whether a parameter value is set.
 * @param {string} param The value of a parameter.
 * @returns {boolean} Whether a parameter value is undefined or not,
 *   meaining whether it has been set on the command-line or not.
 */
function _paramIsSet( param ) {
  return typeof param !== 'undefined';
}

/**
 * Choose the suite based on what command-line flags are passed.
 * @param {Object} params Set of parameters from the command-line.
 * @returns {Array} List of multiCapabilities objects.
 */
function _chooseSuite( params ) {
  const paramsAreNotSet = !_paramIsSet( params.browserName ) &&
                          !_paramIsSet( params.version ) &&
                          !_paramIsSet( params.platform );

  /* Set the capabilities to use the essential suite,
     unless Sauce Labs credentials are set and
     no browser/platform flags are passed, in which case use the full suite.
     This will make it so that setting the browser/platform flags
     won't launch several identical browsers performing the same tests. */
  let capabilities = defaultSuites.essential;

  if ( _useHeadlessChrome() ) {
    capabilities = defaultSuites.headless;
    const cucumberOpts = minimist( process.argv.slice( 2 ) )
      .cucumberOpts || {};
    const WINDOW_SIZES = environmentTest.WINDOW_SIZES;
    let windowWidthPx = WINDOW_SIZES.DESKTOP.WIDTH;
    let windowHeightPx = WINDOW_SIZES.DESKTOP.HEIGHT;

    if ( cucumberOpts.tags === '@mobile' ) {
      windowWidthPx = WINDOW_SIZES.MOBILE.WIDTH;
      windowHeightPx = WINDOW_SIZES.MOBILE.HEIGHT;
    }
    const windowSize = `--window-size=${ windowWidthPx }x${ windowHeightPx }`;
    capabilities[0].chromeOptions.args.push( windowSize );

    if ( envvars.CI ) {
      capabilities[0].chromeOptions.args.push( '--no-sandbox' );
    }
  } else if ( paramsAreNotSet && _useSauceLabs() ) {
    capabilities = defaultSuites.full;
  }

  return capabilities;
}

/**
 * Check that Sauce Labs credentials are set in the .env file
 * and the sauce param is set to true.
 *
 * @returns {boolean} True if all the Sauce credentials
 *   are set and the sauce param is set to true.
 */
function _useSauceLabs() {
  const sauceUsername = envvars.SAUCE_USERNAME;
  const sauceAccessKey = envvars.SAUCE_ACCESS_KEY;
  const sauceTunnel = envvars.SAUCE_TUNNEL;

  const isSauceCredentialsSet = typeof sauceTunnel !== 'undefined' &&
                                sauceTunnel !== '' &&
                                typeof sauceUsername !== 'undefined' &&
                                sauceUsername !== '' &&
                                typeof sauceAccessKey !== 'undefined' &&
                                sauceAccessKey !== '';
  const sauceParam = ( minimist( process.argv ).params || {} ).sauce;
  const isSauceParamSet = sauceParam && sauceParam === 'true';

  return isSauceCredentialsSet && isSauceParamSet;
}

/**
 * Check that headless param is set to true.
 *
 * @returns {boolean} True if headless param is set to true.
 */
function _useHeadlessChrome() {
  const headlessParam = ( minimist( process.argv ).params || {} ).headless;
  const isHeadlessParamSet = headlessParam && headlessParam === 'true';

  return isHeadlessParamSet;
}

/**
 * Choose test specs based on passed parameters.
 * @param {Object} params Set of parameters from the command-line.
 * @returns {Array} List of specs or spec patterns to execute.
 */
function _chooseProtractorSpecs( params ) {
  let i;
  let len;
  let specs = [];

  // If one or more suites are specified, use their specs.
  if ( _paramIsSet( params.suite ) ) {
    const suiteNames = params.suite.split( ',' );
    for ( i = 0, len = suiteNames.length; i < len; i++ ) {
      const suiteSpecs = environmentTest.suites[suiteNames[i]];
      if ( suiteSpecs ) {
        specs = specs.concat( suiteSpecs );
      }
    }
  // Otherwise if specs are specified, use them.
  } else if ( _paramIsSet( params.specs ) ) {
    const specPatterns = params.specs.split( ',' );
    for ( i = 0, len = specPatterns.length; i < len; i++ ) {
      specs = specs.concat( environmentTest.specsBasePath + specPatterns[i] );
    }
  // If neither a suite or specs are specified, use the default suite.
  } else {
    specs = specs.concat( environmentTest.suites.default );
  }

  return specs;
}

/**
 * Params that need to be passed to protractor config.
 * @param {Object} params Set of parameters from the command-line.
 * @returns {Object} Parsed parameters from the command-line,
 *   which are only applicable to protractor.
 */
function _retrieveProtractorParams( params ) { // eslint-disable-line complexity, no-inline-comments, max-len
  const parsedParams = {};

  parsedParams.specs = _chooseProtractorSpecs( params );

  if ( _paramIsSet( params.browserName ) ) {
    parsedParams.browserName = params.browserName;
  }

  if ( _paramIsSet( params.version ) ) {
    parsedParams.version = params.version;
  }

  if ( _paramIsSet( params.platform ) ) {
    parsedParams.platform = params.platform;
  }

  return parsedParams;
}

/**
 * Copy parameters into multiCapabilities array.
 * @param {Object} params Set of parameters from the command-line.
 * @param {Array} capabilities List of multiCapabilities objects.
 * @returns {Array} List of multiCapabilities objects
 *   with injected params from the command-line and a test name field.
 */
function _copyParameters( params, capabilities ) { // eslint-disable-line complexity, no-inline-comments, max-len
  const newCapabilities = [];
  const injectParams = _retrieveProtractorParams( params );
  let capability;

  for ( let i = 0, len = capabilities.length; i < len; i++ ) {
    capability = capabilities[i];
    for ( const p in injectParams ) {
      if ( injectParams.hasOwnProperty( p ) ) {
        capability[p] = injectParams[p];
      }
    }
    capability.name = environmentTest.testName +
                      ' ' + capability.specs +
                      ', running ' +
                      capability.browserName +
                      ( String( capability.version ).length > 0 ?
                        ' ' + capability.version : '' ) +
                      ' on ' + capability.platform +
                      ' at ' +
                      ( params.windowSize ?
                        params.windowSize :
                        environmentTest.windowWidthPx + ',' +
                        environmentTest.windowHeightPx ) + 'px';
    newCapabilities.push( capability );
  }

  return newCapabilities;
}

/**
 * The getMultiCapabilities method for Protractor's workflow.
 * See https://github.com/angular/protractor/blob/master/lib/config.ts#L336
 * @returns {Object} Selenium configuration object.
 */
function _getMultiCapabilities() {
  const params = this.params;
  const suite = _chooseSuite( params );
  const capabilities = _copyParameters( params, suite );

  return capabilities;
}


/**
 * The onPrepare method for Protractor's workflow.
 * See https://github.com/angular/protractor/blob/master/docs/system-setup.md
 */
function _onPrepare() {
  retry.onPrepare();
  // Ignore Selenium allowances for non-angular sites.
  browser.ignoreSynchronization = true;

  /* If --windowSize=w,h flag was passed, set window dimensions.
     Otherwise, use default values from the test settings. */
  const windowSize = browser.params.windowSize;
  const WINDOW_SIZES = environmentTest.WINDOW_SIZES;
  const cucumberOpts = minimist( process.argv.slice( 2 ) ).cucumberOpts || {};

  let windowWidthPx = WINDOW_SIZES.DESKTOP.WIDTH;
  let windowHeightPx = WINDOW_SIZES.DESKTOP.HEIGHT;

  if ( windowSize ) {
    const windowSizeArray = windowSize.split( ',' );
    windowWidthPx = Number( windowSizeArray[0] );
    windowHeightPx = Number( windowSizeArray[1] );
  } else if ( cucumberOpts.tags === '@mobile' ) {
    windowWidthPx = WINDOW_SIZES.MOBILE.WIDTH;
    windowHeightPx = WINDOW_SIZES.MOBILE.HEIGHT;
  }

  /* Calling setSize with headless chromeDriver doesn't work properly if
     the requested size is larger than the available screen size. */
  if ( _useHeadlessChrome() === false ) {
    browser.driver.manage().window().setSize(
      windowWidthPx,
      windowHeightPx
    );

    // Set default windowSize parameter equal to the value in settings.js.
    browser.params.windowWidth = windowWidthPx;
    browser.params.windowHeight = windowHeightPx;
    browser.params.windowSize = String( windowWidthPx ) +
                                ',' + String( windowHeightPx );
  }
}

const config = {
  baseUrl:                  environmentTest.baseUrl,
  cucumberOpts: {
    'require':   'cucumber/step_definitions/**/*.js',
    'tags':      [ '~@mobile', '~@skip', '~@undefined' ],
    'profile':   false,
    'no-source': true,
    'fail-fast': true
  },
  afterLaunch:              () => retry.afterLaunch( 1 ),
  directConnect:            true,
  framework:                'custom',
  frameworkPath:            require.resolve( 'protractor-cucumber-framework' ),
  getMultiCapabilities:     _getMultiCapabilities,
  onCleanUp:                results => retry.onCleanUp( results ),
  onPrepare:                _onPrepare,
  SELENIUM_PROMISE_MANAGER: false,
  unknownFlags_:            [ 'cucumberOpts' ]
};

// Set Sauce Labs credientials from .env file.
if ( _useSauceLabs() ) {
  config.sauceUser = envvars.SAUCE_USERNAME;
  config.sauceKey = envvars.SAUCE_ACCESS_KEY;
  config.directConnect = false;
}

exports.config = config;
