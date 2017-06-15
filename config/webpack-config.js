/* ==========================================================================
   Settings for webpack JavaScript bundling system.
   ========================================================================== */

'use strict';

var BannerFooterPlugin = require( 'banner-footer-webpack-plugin' );
var path = require( 'path' );
var paths = require( '../config/environment' ).paths;
var scriptsManifest = require( '../gulp/utils/scripts-manifest' );
var webpack = require( 'webpack' );

// Constants.
var JS_ROUTES_PATH = '/js/routes';
var COMMON_BUNDLE_NAME = 'common.js';

var modernConf = {
  cache: true,
  context: path.join( __dirname, '/../', paths.unprocessed, JS_ROUTES_PATH ),
  entry: scriptsManifest.getDirectoryMap( paths.unprocessed + JS_ROUTES_PATH ),
  module: {
    rules: [ {
      test: /\.js$/,
      use: [ {
        loader: 'babel-loader?cacheDirectory=true'
      } ],
      exclude: /node_modules/
    } ]
  },
  output: {
    path: path.join( __dirname, 'js' ),
    filename: '[name]'
  },
  plugins: [
    new webpack.optimize.CommonsChunkPlugin( {
      name: COMMON_BUNDLE_NAME
    } ),
    // Change `warnings` flag to true to view linter-style warnings at runtime.
    new webpack.optimize.UglifyJsPlugin( {
      compress: { warnings: false }
    } ),
    // Wrap JS in raw Jinja tags so included JS won't get parsed by Jinja.
    new BannerFooterPlugin( '{% raw %}', '{% endraw %}', { raw: true } )
  ]
};

var ieConf = {
  entry: paths.unprocessed + '/js/ie/common.ie.js',
  output: {
    filename: 'common.ie.js'
  },
  plugins: [
    new webpack.optimize.UglifyJsPlugin( {
      compress: { warnings: false }
    } )
  ]
};

var externalConf = {
  entry: paths.unprocessed + JS_ROUTES_PATH + '/external-site/index.js',
  output: {
    filename: 'external-site.js'
  },
  plugins: [
    new webpack.optimize.UglifyJsPlugin( {
      compress: { warnings: false }
    } )
  ]
};

var onDemandConf = {
  context: path.join( __dirname, '/../', paths.unprocessed,
                      JS_ROUTES_PATH + '/on-demand' ),
  entry:   scriptsManifest.getDirectoryMap( paths.unprocessed +
                                            JS_ROUTES_PATH + '/on-demand' ),
  output: {
    path:     path.join( __dirname, 'js' ),
    filename: '[name]'
  },
  plugins: [
    // Change warnings flag to true to view linter-style warnings at runtime.
    new webpack.optimize.UglifyJsPlugin( {
      compress: { warnings: false }
    } )
  ]
};

var onDemandHeaderRawConf = {
  context: path.join( __dirname, '/../', paths.unprocessed,
                      JS_ROUTES_PATH + '/on-demand' ),
  entry:   './header.js',
  output: {
    path:     path.join( __dirname, 'js' ),
    filename: '[name]'
  }
};

var spanishConf = {
  entry: paths.unprocessed + JS_ROUTES_PATH + '/es/obtener-respuestas/single.js',
  output: {
    filename: 'spanish.js'
  },
  plugins: [
    new webpack.optimize.UglifyJsPlugin( {
      compress: { warnings: false }
    } )
  ]
};

module.exports = {
  onDemandHeaderRawConf: onDemandHeaderRawConf,
  onDemandConf:          onDemandConf,
  ieConf:                ieConf,
  modernConf:            modernConf,
  externalConf:          externalConf,
  spanishConf:           spanishConf
};
