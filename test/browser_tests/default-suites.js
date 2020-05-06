const envvars = require( '../../config/environment' ).envvars;
const tunnelIdentifier = envvars.SAUCE_TUNNEL;

const defaultSuites = {

  /* Set default browser suites to test.
     These values are passed to the `multiCapabilities` property
     of the protractor config object.
     See https://docs.saucelabs.com/reference/platforms-configurator/
     for configuration values for version and platform. */

  // Essential browsers for running locally.
  essential: [
    {
      browserName:      'chrome',
      extendedDebugging: true,
      maxDuration:      10800,
      maxInstances:     4,
      platform:         'Windows',
      shardTestFiles:   true,
      tunnelIdentifier: tunnelIdentifier,
      version:          ''
    }
  ],

  // Legacy browsers to run in the cloud.
  legacy: [
    {
      browserName:      'internet explorer',
      maxDuration:      10800,
      maxInstances:     2,
      platform:         'Windows 7',
      shardTestFiles:   true,
      tunnelIdentifier: tunnelIdentifier,
      version:          '10.0'
    }
  ],

  // Modern browsers to run in the cloud.
  modern: [
    {
      'browserName':      'firefox',
      'marionette':       false,
      'native':           false,
      'maxDuration':      10800,
      'maxInstances':     2,
      'platform':         'Windows 10',
      'shardTestFiles':   true,
      'tunnelIdentifier': tunnelIdentifier,
      'version':          ''
    },
    {
      browserName:                 'internet explorer',
      ignoreProtectedModeSettings: true,
      ignoreZoomSetting:           true,
      maxDuration:                 10800,
      maxInstances:                2,
      nativeEvents:                false,
      platform:                    'Windows 10',
      shardTestFiles:              true,
      tunnelIdentifier:            tunnelIdentifier,
      version:                     ''
    }
  ],

  // Headless browser to run on CI.
  headless: [
    {
      browserName:   'chrome',
      chromeOptions: {
        args: [ '--headless', '--disable-gpu' ]
      },
      maxDuration:    10800
    }
  ]
};

// Run all browsers together.
defaultSuites.full = defaultSuites.essential.concat(
  defaultSuites.modern,
  defaultSuites.legacy
);

module.exports = defaultSuites;
