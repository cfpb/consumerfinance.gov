/* ==========================================================================
   Settings for webpack JavaScript bundling system.
   ========================================================================== */

'use strict';

const BannerFooterPlugin = require( 'banner-footer-webpack-plugin' );
const path = require( 'path' );
const environment = require( '../config/environment' );
const paths = environment.paths;
const scriptsManifest = require( '../gulp/utils/scripts-manifest' );
const webpack = require( 'webpack' );
const UglifyWebpackPlugin = require( 'uglifyjs-webpack-plugin' );

// Constants.
const JS_ROUTES_PATH = '/js/routes';
const COMMON_BUNDLE_NAME = 'common.js';

const modernConf = {
  cache: true,
  context: path.join( __dirname, '/../', paths.unprocessed, JS_ROUTES_PATH ),
  entry: scriptsManifest.getDirectoryMap( paths.unprocessed + JS_ROUTES_PATH ),
  module: {
    rules: [ {
      test: /\.js$/,
      use: [ {
        loader: 'babel-loader?cacheDirectory=true',
        options: {
          presets: [ [ 'env', {
            targets: {
              browsers: environment.getSupportedBrowserList()
            },
            debug: true,
            // See https://stackoverflow.com/a/45088328 and
            // https://github.com/babel/babel-preset-env/tree/v2.0.0-alpha.19#forcealltransforms
            // Webpack's uglify plugin doesn't play nicely with ES6.
            // Eventually we should migrate to https://github.com/babel/minify
            forceAllTransforms: true
          } ] ]
        }
      } ],
      exclude: {
        test: /node_modules/,
        exclude: /node_modules\/cfpb-chart-builder(\-\w+)?/
      }
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
    new UglifyWebpackPlugin( {
      compress: { warnings: false }
    } ),
    // Wrap JS in raw Jinja tags so included JS won't get parsed by Jinja.
    new BannerFooterPlugin( '{% raw %}', '{% endraw %}', { raw: true } )
  ]
};

const ieConf = {
  entry: paths.unprocessed + '/js/ie/common.ie.js',
  output: {
    filename: 'common.ie.js'
  },
  plugins: [
    new UglifyWebpackPlugin( {
      compress: { warnings: false }
    } )
  ]
};

const externalConf = {
  entry: paths.unprocessed + JS_ROUTES_PATH + '/external-site/index.js',
  output: {
    filename: 'external-site.js'
  },
  plugins: [
    new UglifyWebpackPlugin( {
      compress: { warnings: false }
    } )
  ]
};

const onDemandConf = {
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
    new UglifyWebpackPlugin( {
      compress: { warnings: false }
    } )
  ]
};

const onDemandHeaderRawConf = {
  context: path.join( __dirname, '/../', paths.unprocessed,
                      JS_ROUTES_PATH + '/on-demand' ),
  entry:   './header.js',
  output: {
    path:     path.join( __dirname, 'js' ),
    filename: '[name]'
  }
};

const spanishConf = {
  entry: paths.unprocessed + JS_ROUTES_PATH + '/es/obtener-respuestas/single.js',
  output: {
    filename: 'spanish.js'
  },
  plugins: [
    new UglifyWebpackPlugin( {
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
