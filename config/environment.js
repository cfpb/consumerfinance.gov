/* ==========================================================================
   Settings for project environment.
   Used by JavaScript gulp build process and JavaScript test configuration.
   ========================================================================== */

'use strict';

/**
 * Environment variable mappings in JavaScript from the project root .env file.
 */
const envvars = {

  /* eslint-disable no-process-env */
  DJANGO_STAGING_HOSTNAME: process.env.DJANGO_STAGING_HOSTNAME,
  TEST_HTTP_HOST:          process.env.TEST_HTTP_HOST,
  TEST_HTTP_PORT:          process.env.DJANGO_HTTP_PORT,
  SAUCE_SELENIUM_URL:      process.env.SAUCE_SELENIUM_URL,
  SAUCE_USERNAME:          process.env.SAUCE_USERNAME,
  SAUCE_ACCESS_KEY:        process.env.SAUCE_ACCESS_KEY,
  ACHECKER_ID:             process.env.ACHECKER_ID,
  HEADLESS_CHROME_BINARY:  process.env.HEADLESS_CHROME_BINARY,
  SAUCE_TUNNEL:            process.env.SAUCE_TUNNEL ||
                           new Date().getTime()
  /* eslint-enable no-process-env */
};


/**
 * @description
 * Browser list for autoprefixer, see https://github.com/ai/browserslist.
 * @returns {array} List of supported browser strings.
 */
function getSupportedBrowserList() {
  return [
    'last 2 version',
    'Edge >= 11',
    'not ie <= 8',
    'android 4',
    'BlackBerry 7',
    'BlackBerry 10'
  ];
}

/**
 * Convenience settings for various project directory paths.
 */
const paths = {
  unprocessed: './cfgov/unprocessed',
  processed:   './cfgov/static_built',
  legacy:      './cfgov/legacy/static',
  lib:         './vendor',
  modules:     './node_modules',
  test:        './test'
};

module.exports = {
  envvars: envvars,
  getSupportedBrowserList: getSupportedBrowserList,
  paths: paths
};
