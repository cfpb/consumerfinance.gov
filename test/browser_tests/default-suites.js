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
      version:          '',
      platform:         'Windows',
      maxDuration:      10800,
      tunnelIdentifier: tunnelIdentifier
    }
  ],

  // Legacy browsers to run in the cloud.
  legacy: [
    {
      browserName:      'internet explorer',
      version:          '9.0',
      platform:         'Windows 7',
      maxDuration:      10800,
      tunnelIdentifier: tunnelIdentifier
    },
    {
      browserName:      'internet explorer',
      version:          '10.0',
      platform:         'Windows 7',
      maxDuration:      10800,
      tunnelIdentifier: tunnelIdentifier
    }
  ],

  // Modern browsers to run in the cloud.
  modern: [
    {
      browserName:      'firefox',
      version:          '',
      platform:         'Windows 10',
      maxDuration:      10800,
      tunnelIdentifier: tunnelIdentifier
    },
    {
      browserName:      'internet explorer',
      version:          '',
      platform:         'Windows 10',
      maxDuration:      10800,
      tunnelIdentifier: tunnelIdentifier
    }
  ],

  // Headless browser to run on Travis.
  headless: [
    {
      browserName:   'chrome',
      chromeOptions: {
        args: [ '--headless', '--disable-gpu' ]
      },
      maxDuration: 10800
    }
  ]
};


// Run all browsers together.
defaultSuites.full = defaultSuites.essential.concat(
  defaultSuites.modern,
  defaultSuites.legacy
);

module.exports = defaultSuites;
