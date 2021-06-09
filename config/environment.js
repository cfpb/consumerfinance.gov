/* ==========================================================================
   Settings for project environment.
   Used by JavaScript gulp build process and JavaScript test configuration.
   ========================================================================== */


/**
 * Environment variable mappings in JavaScript from the project root .env file.
 */
const envvars = {
  /* eslint-disable no-process-env */
  NODE_ENV: process.env.NODE_ENV
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
