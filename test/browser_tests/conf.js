'use strict';

var environment = require( './environment.js' );
var defaultSuites = require( './default-suites.js' );

/**
 * Check whether a parameter value is set.
 * @param {string} param The value of a parameter.
 * @returns {Boolean} Whether a parameter value is undefined or not,
 *   meaining whether it has been set on the command-line or not.
 */
function _paramIsSet( param ) {
  return typeof param !== 'undefined';
}

/**
 * Choose the suite based on what command-line flags are passed.
 * @param {object} params Set of parameters from the command-line.
 * @returns {Array} List of multiCapabilities objects.
 */
function _chooseSuite( params ) {


  var paramsAreNotSet = !_paramIsSet( params.browserName ) &&
                        !_paramIsSet( params.version ) &&
                        !_paramIsSet( params.platform );

  var useSauceCredentials = ( !_paramIsSet( params.sauce ) ||
                              params.sauce === 'true' ) &&
                            _isSauceCredentialSet();

  // Set the capabilities to use the essential suite,
  // unless Sauce Labs credentials are set and
  // no browser/platform flags are passed, in which case use the full suite.
  // This will make it so that setting the browser/platform flags
  // won't launch several identical browsers performing the same tests.
  var capabilities = defaultSuites.essential;
  if ( paramsAreNotSet && useSauceCredentials ) {
    capabilities = defaultSuites.full;
  }

  return capabilities;
}

/**
 * Check that Sauce Labs credentials are set in the .env file.
 * @returns {Boolean} True if all the Sauce credentials
 *   are not undefined or an empty string, false otherwise.
 */
function _isSauceCredentialSet() {
  var sauceSeleniumUrl = process.env.SAUCE_SELENIUM_URL;
  var sauceUsername = process.env.SAUCE_USERNAME;
  var sauceAccessKey = process.env.SAUCE_ACCESS_KEY;

  return typeof sauceSeleniumUrl !== 'undefined' &&
         sauceSeleniumUrl !== '' &&
         typeof sauceUsername !== 'undefined' &&
         sauceUsername !== '' &&
         typeof sauceAccessKey !== 'undefined' &&
         sauceAccessKey !== '';
}

/**
 * Choose test specs based on passed parameters.
 * @param {object} params Set of parameters from the command-line.
 * @returns {Array} List of specs or spec patterns to execute.
 */
function _chooseProtractorSpecs( params ) {
  var i;
  var len;
  var specs = [];

  // If one or more suites are specified, use their specs.
  if ( _paramIsSet( params.suite ) ) {
    var suiteNames = params.suite.split( ',' );
    for ( i = 0, len = suiteNames.length; i < len; i++ ) {
      var suiteSpecs = environment.suites[suiteNames[i]];
      if ( suiteSpecs ) {
        specs = specs.concat( suiteSpecs );
      }
    }
  // Otherwise if specs are specified, use them.
  } else if ( _paramIsSet( params.specs ) ) {
    var specPatterns = params.specs.split( ',' );
    for ( i = 0, len = specPatterns.length; i < len; i++ ) {
      specs = specs.concat( environment.specsBasePath + specPatterns[i] );
    }
  // If neither a suite or specs are specified, use all specs.
  } else {
    specs = specs.concat( environment.specsBasePath + '.js' );
  }

  return specs;
}

/**
 * Params that need to be passed to protractor config.
 * @param {object} params Set of parameters from the command-line.
 * @returns {object} Parsed parameters from the command-line,
 *   which are only applicable to protractor.
 */
function _retrieveProtractorParams( params ) { // eslint-disable-line complexity, no-inline-comments, max-len
  var parsedParams = {};

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
 * @param {object} params Set of parameters from the command-line.
 * @param {Array} capabilities List of multiCapabilities objects.
 * @returns {Array} List of multiCapabilities objects
 *   with injected params from the command-line and a test name field.
 */
function _copyParameters( params, capabilities ) { // eslint-disable-line complexity, no-inline-comments, max-len
  var newCapabilities = [];
  var injectParams = _retrieveProtractorParams( params );
  var capability;
  for ( var i = 0, len = capabilities.length; i < len; i++ ) {
    capability = capabilities[i];
    for ( var p in injectParams ) {
      if ( injectParams.hasOwnProperty( p ) ) {
        capability[p] = injectParams[p];
      }
    }
    capability.name = environment.testName +
                      ' ' + capability.specs +
                      ', running ' +
                      capability.browserName +
                      ( String( capability.version ).length > 0 ?
                        ' ' + capability.version : '' ) +
                      ' on ' + capability.platform +
                      ' at ' +
                      ( params.windowSize ?
                        params.windowSize :
                        environment.windowWidthPx + ',' +
                        environment.windowHeightPx ) + 'px';
    newCapabilities.push( capability );
  }

  return newCapabilities;
}

var config = {
  baseUrl:         environment.baseUrl,
  framework:       'jasmine2',
  jasmineNodeOpts: {
    defaultTimeoutInterval: 60000
  },

  getMultiCapabilities: function() {
    var params = this.params;

    // If Sauce Labs credentials or --sauce flag is not set or is not true,
    // delete Sauce credentials on the config object.
    if ( !_isSauceCredentialSet() || params.sauce === 'false' ) {
      delete config.sauceSeleniumAddress;
      delete config.sauceUser;
      delete config.sauceKey;
    }

    var suite = _chooseSuite( params );
    var capabilities = _copyParameters( params, suite );
    return capabilities;
  },

  onPrepare: function() {
    browser.ignoreSynchronization = true;

    // If --windowSize=w,h flag was passed, set window dimensions.
    // Otherwise, use default values from the test settings.
    var windowSize = browser.params.windowSize;
    var windowWidthPx;
    var windowHeightPx;
    if ( typeof windowSize === 'undefined' ) {
      windowWidthPx = environment.windowWidthPx;
      windowHeightPx = environment.windowHeightPx;
    } else {
      var windowSizeArray = windowSize.split( ',' );
      windowWidthPx = Number( windowSizeArray[0] );
      windowHeightPx = Number( windowSizeArray[1] );
    }

    browser.driver.manage().window().setSize(
      windowWidthPx,
      windowHeightPx
    );

    // Set default windowSize parameter equal to the value in settings.js.
    browser.params.windowWidth = windowWidthPx;
    browser.params.windowHeight = windowHeightPx;
    browser.params.windowSize = String( windowWidthPx ) +
                                ',' + String( windowHeightPx );

    browser.getProcessedConfig().then( function( cf ) {
      console.log( 'Executing...', cf.capabilities.name ); // eslint-disable-line no-console, no-inline-comments, max-len
    } );
    return;
  }
};

// Set Sauce Labs credientials from .env file.
if ( _isSauceCredentialSet() ) {
  config.sauceSeleniumAddress = process.env.SAUCE_SELENIUM_URL;
  config.sauceUser = process.env.SAUCE_USERNAME;
  config.sauceKey = process.env.SAUCE_ACCESS_KEY;
}

exports.config = config;
