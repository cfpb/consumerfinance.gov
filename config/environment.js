/* ==========================================================================
   Settings for project environment.
   Used by JavaScript gulp build process and JavaScript test configuration.
   ========================================================================== */

'use strict';

/**
 * Environment variable mappings in JavaScript from the project root .env file.
 */
var envvars = {

  /* eslint-disable no-process-env */
  DJANGO_STAGING_HOSTNAME: process.env.DJANGO_STAGING_HOSTNAME,
  TEST_HTTP_HOST:          process.env.TEST_HTTP_HOST,
  TEST_HTTP_PORT:          process.env.TEST_HTTP_PORT,
  SAUCE_SELENIUM_URL:      process.env.SAUCE_SELENIUM_URL,
  SAUCE_USERNAME:          process.env.SAUCE_USERNAME,
  SAUCE_ACCESS_KEY:        process.env.SAUCE_ACCESS_KEY,
  ACHECKER_ID:             process.env.ACHECKER_ID

  /* eslint-enable no-process-env */
};

/**
 * Convenience settings for various project directory paths.
 */
var paths = {
  unprocessed: './cfgov/unprocessed',
  processed:   './cfgov/static_built',
  legacy:      './cfgov/legacy/static',
  lib:         './vendor',
  modules:     './node_modules',
  test:        './test'
};

module.exports = {
  envvars: envvars,
  paths: paths
};
