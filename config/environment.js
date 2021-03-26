/* ==========================================================================
   Settings for project environment.
   Used by JavaScript gulp build process and JavaScript test configuration.
   ========================================================================== */


/**
 * Environment variable mappings in JavaScript from the project root .env file.
 */
const envvars = {

  /* eslint-disable no-process-env */
  NODE_ENV:                process.env.NODE_ENV,
  TEST_HTTP_HOST:          process.env.TEST_HTTP_HOST,
  TEST_HTTP_PORT:          process.env.DJANGO_HTTP_PORT,
  SAUCE_SELENIUM_URL:      process.env.SAUCE_SELENIUM_URL,
  SAUCE_USERNAME:          process.env.SAUCE_USERNAME,
  SAUCE_ACCESS_KEY:        process.env.SAUCE_ACCESS_KEY,
  SAUCE_TUNNEL:            process.env.SAUCE_TUNNEL
  /* eslint-enable no-process-env */
};

/**
 * Convenience settings for various project directory paths.
 */
const paths = {
  unprocessed: './cfgov/unprocessed',
  processed:   './cfgov/static_built',
  modules:     './node_modules',
  test:        './test'
};

module.exports = {
  envvars,
  paths
};
