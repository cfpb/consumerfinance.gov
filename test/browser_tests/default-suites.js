'use strict';

var environment = require( './environment.js' );

var defaultSuites = {
  // Set default browser suites to test.
  // These values are passed to the `multiCapabilities` property
  // of the protractor config object.
  // See https://docs.saucelabs.com/reference/platforms-configurator/
  // for configuration values for version and platform.

  // Essential browsers for running locally.
  essential: [
    {
      specs:       [ environment.specsBasePath + '*.js' ],
      browserName: 'chrome',
      version:     '',
      platform:    'Windows',
      maxDuration: 10800
    }
  ],

  // Legacy browsers to run in the cloud.
  legacy: [
    {
      specs:       [ environment.specsBasePath + '*.js' ],
      browserName: 'internet explorer',
      version:     '8.0',
      platform:    'Windows XP',
      maxDuration: 10800
    }
  ],

  // Modern browsers to run in the cloud.
  modern: [
    {
      specs:       [ environment.specsBasePath + '*.js' ],
      browserName: 'firefox',
      version:     '',
      platform:    'Windows 10',
      maxDuration: 10800
    },
    {
      specs:       [ environment.specsBasePath + '*.js' ],
      browserName: 'internet explorer',
      version:     '',
      platform:    'Windows 10',
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
