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
  // jQuery is imported globally in the HTML head section in base.html,
  // so it needs to be defined here as an external script to ignore for
  // unmet dependency references.
  externals: { jquery: 'jQuery' },
  context:   path.join( __dirname, '/../', paths.unprocessed, JS_ROUTES_PATH ),
  entry:     scriptsManifest.getDirectoryMap( paths.unprocessed +
                                              JS_ROUTES_PATH ),
  output: {
    path:     path.join( __dirname, 'js' ),
    filename: '[name]'
  },
  plugins: [
    new webpack.optimize.CommonsChunkPlugin( COMMON_BUNDLE_NAME ),
    new webpack.optimize.CommonsChunkPlugin( COMMON_BUNDLE_NAME,
                                             [ COMMON_BUNDLE_NAME ] ),
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

module.exports = {
  onDemandHeaderRawConf: onDemandHeaderRawConf,
  onDemandConf:          onDemandConf,
  ieConf:                ieConf,
  modernConf:            modernConf,
  externalConf:          externalConf
};
