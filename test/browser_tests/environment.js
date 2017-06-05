'use strict';

var envvars = require( '../../config/environment' ).envvars;
var specsRoot = 'cucumber/features/';

module.exports = {
  // A base URL for your application under test.
  baseUrl: 'http://' + envvars.TEST_HTTP_HOST + ':' + envvars.TEST_HTTP_PORT,

  // The base path where the spec suites are located.
  specsBasePath: specsRoot + '**/*',

  suites: {
    'default': [
      specsRoot + 'suites/default/*.feature'
    ],
    'wagtail-admin': [
      'cucumber/features/suites/wagtail-admin/*.feature'
    ]
  },

  // The default window width and height.
  // Can be overridden with the --windowSize=w,h command-line flag.
  windowWidthPx:  1200,
  windowHeightPx: 900,

  // Default test name, which displays in Sauce Labs and the Terminal.
  testName: 'cfgov-refresh screen test'
};
