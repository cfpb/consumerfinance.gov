'use strict';

var envvars = require( '../../config/environment' ).envvars;
var specsRoot = 'spec_suites/';

module.exports = {
  // A base URL for your application under test.
  baseUrl: 'http://consumerfinance.gov',

  // The base path where the spec suites are located.
  specsBasePath: specsRoot + '**/*',

  suites: {
    integration: [
      specsRoot + 'integration/**/*.js'
    ],
    content: [
      specsRoot + 'content/**/*.js'
    ]
  },

  // The default window width and height.
  // Can be overridden with the --windowSize=w,h command-line flag.
  windowWidthPx:  1200,
  windowHeightPx: 900,

  // Default test name, which displays in Sauce Labs and the Terminal.
  testName: 'cfgov-refresh screen test'
};
