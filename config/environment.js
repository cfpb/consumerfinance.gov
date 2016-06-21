/* ==========================================================================
   Settings for project environment. Used by JavaScript gulp build process.
   ========================================================================== */

'use strict';

var paths = {
  unprocessed: './cfgov/unprocessed',
  processed:   './cfgov/static_built',
  legacy: 	   './cfgov/legacy/static',
  lib:         './vendor',
  modules:     './node_modules',
  test:        './test'
};

module.exports = {
  paths: paths
};
