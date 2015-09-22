/* ==========================================================================
   Settings for webpack JavaScript bundling system.
   ========================================================================== */

'use strict';

var BannerFooterPlugin = require('banner-footer-webpack-plugin');
var path = require( 'path' );
var paths = require( '../config/environment' ).paths;
var scriptsManifest = require( '../gulp/utils/scriptsManifest' );
var webpack = require( 'webpack' );

// Constants.
var JS_ROUTES_PATH = '/js/routes';
var COMMON_BUNDLE_NAME = 'common.js';

module.exports = {
  // jQuery is exported in the global space in the head.
  externals: { jquery: "jQuery" },
  context: __dirname + '/../' + paths.preproccesed + JS_ROUTES_PATH,
  entry: scriptsManifest.getDirectoryMap( paths.preproccesed + JS_ROUTES_PATH ),
  output: {
    path: path.join(__dirname, 'js'),
    filename: '[name]'
  },
  plugins: [
    new webpack.optimize.CommonsChunkPlugin( COMMON_BUNDLE_NAME ),
    new webpack.optimize.CommonsChunkPlugin( COMMON_BUNDLE_NAME,
                                             [COMMON_BUNDLE_NAME] ),
    // Change warnings flag to true to view linter-style warnings at runtime.
    new webpack.optimize.UglifyJsPlugin( { compress: { warnings: false } } ),
    // Wrap JS in raw Jinja tags so included JS won't get parsed by Jinja.
    new BannerFooterPlugin( '{% raw %}', '{% endraw %}', { raw: true } )
  ],
  module: {
    loaders: [
      // Disable incompatible AMD pattern in dateformat module.
      { test: require.resolve( 'dateformat' ), loader: 'imports?define=>false' }
    ]
  },
};
