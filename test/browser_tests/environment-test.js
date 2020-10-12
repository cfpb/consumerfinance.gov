const envvars = require( '../../config/environment' ).envvars;
const specsRoot = 'cucumber/features/';

module.exports = {
  // A base URL for your application under test.
  baseUrl: 'http://' + envvars.TEST_HTTP_HOST + ':' + envvars.TEST_HTTP_PORT,

  // The base path where the spec suites are located.
  specsBasePath: specsRoot + '**/*',

  suites: {
    'apps': [
      specsRoot + 'suites/apps/**/*.feature'
    ],
    'default': [
      specsRoot + 'suites/default/**/*.feature'
    ]
  },

  /* The default window width and height.
     Can be overridden with the --windowSize=w,h command-line flag. */
  WINDOW_SIZES: {
    DESKTOP: {
      WIDTH:  1200,
      HEIGHT: 900
    },
    TABLET: {
      WIDTH:  768,
      HEIGHT: 1024
    },
    MOBILE: {
      WIDTH:  600,
      HEIGHT: 740
    }
  },

  // Default test name, which displays in Sauce Labs and the Terminal.
  testName: 'consumerfinance.gov screen test'
};
