/* ==========================================================================
   Settings for webpack JavaScript bundling system.
   ========================================================================== */

'use strict';

var path = require( 'path' );
var paths = require( '../config/environment' ).paths;
var jsManifest = require( '../' + paths.src + '/static/js/config/js-manifest-config' );
var scriptsManifest = require( '../gulp/utils/scriptsManifest' );
var webpack = require( 'webpack' );

scriptsManifest.writeScriptsManifest( paths.dist + jsManifest.writePath,
                                      jsManifest.filename,
                                      paths.src + jsManifest.readPath );

module.exports = {
  // jQuery is exported in the global space in the head.
  externals: { jquery: "jQuery" },
  context: __dirname + '/../' + paths.src + jsManifest.readPath,
  entry: scriptsManifest.getDirectoryMap( paths.src + jsManifest.readPath ),
  output: {
    path: path.join(__dirname, 'js'),
    filename: '[name]'
  },
  plugins: [
    new webpack.optimize.CommonsChunkPlugin( jsManifest.commonBundleName ),
    new webpack.optimize.CommonsChunkPlugin( jsManifest.commonBundleName,
                                             [jsManifest.commonBundleName] ),
    // Change warnings flag to true to view linter-style warnings at runtime.
    new webpack.optimize.UglifyJsPlugin( { compress: { warnings: false } } )
  ],
  module: {
    loaders: [
      // Disable incompatible AMD pattern in dateformat module.
      { test: require.resolve( 'dateformat' ), loader: 'imports?define=>false' }
    ]
  },
};
