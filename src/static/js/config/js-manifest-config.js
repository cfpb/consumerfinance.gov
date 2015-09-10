'use strict';

// routes = The location in the distribution directory where the manifest should be placed.
// dir = The directory to traverse when generating the manifest.
// name = the filename of the manifest file.
// templateScriptName = The filename of template JS files.
// commonBundleName = The filename of common bundle JS files.
module.exports = {
  writePath:          '/static/js/',
  readPath:           '/static/js/routes',
  filename:           'routes-manifest.json',
  templateScriptName: 'single.js',
  commonBundleName:   'common.js'
};
