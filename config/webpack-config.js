/* ==========================================================================
   Settings for webpack JavaScript bundling system.
   ========================================================================== */

'use strict';

const path = require( 'path' );
const environment = require( '../config/environment' );
const paths = environment.paths;
const scriptsManifest = require( '../gulp/utils/scripts-manifest' );
const webpack = require( 'webpack' );
const UglifyWebpackPlugin = require( 'uglifyjs-webpack-plugin' );


// Constants.
const JS_ROUTES_PATH = '/js/routes';
const OAH_COMMON_BUNDLE_ROUTE = '/js/routes/owning-a-home/';
const COMMON_BUNDLE_NAME = 'common.js';

// Commmon webpack 'module' option used in each configuration.
// Runs code through Babel and uses global supported browser list.
const COMMON_MODULE_CONFIG = {
  loaders: [ {
    test: /\.js$/,
    loaders: [ {
      loader: 'babel-loader?cacheDirectory=true',
      options: {
        presets: [ [ 'env', {
          targets: {
            browsers: environment.getSupportedBrowserList( 'js' )
          },
          debug: true
        } ] ]
      }
    } ],
    exclude: {
      test: /node_modules/,
      // The below regex will capture all node modules that start with `cf`
      // or atomic-component. Regex test: https://regex101.com/r/zizz3V/1/.
      exclude: /node_modules\/(?:cf.+|atomic-component)/
    }
  } ]
};

 // Set warnings to true to show linter-style warnings.
 // Set mangle to false and beautify to true to debug the output code.
const COMMON_UGLIFY_CONFIG = new UglifyWebpackPlugin( {
  parallel: true,
  uglifyOptions: {
    ie8: false,
    ecma: 5,
    warnings: false,
    mangle: true,
    output: {
      comments: false,
      beautify: false
    }
  }
} );


const COMMON_CHUNK_CONFIG = new webpack.optimize.CommonsChunkPlugin( {
  name: COMMON_BUNDLE_NAME
} );


const commonConf = {
  module: COMMON_MODULE_CONFIG,
  output: {
    filename: '[name]'
  },
  plugins: [
    COMMON_UGLIFY_CONFIG
  ]
};

const externalConf = {
  module: COMMON_MODULE_CONFIG,
  output: {
    filename: 'external-site.js'
  },
  plugins: [
    COMMON_UGLIFY_CONFIG
  ]
};

const modernConf = {
  cache: true,
  module: COMMON_MODULE_CONFIG,
  output: {
    filename: '[name]'
  },
  plugins: [
    COMMON_CHUNK_CONFIG,
    COMMON_UGLIFY_CONFIG
  ]
};

const onDemandHeaderRawConf = {
  module: COMMON_MODULE_CONFIG
};

const owningAHomeConf = {
  cache: true,
  module: COMMON_MODULE_CONFIG,
  output: {
    filename: '[name]',
    jsonpFunction: 'OAH'
  },
  plugins: [
    COMMON_CHUNK_CONFIG,
    COMMON_UGLIFY_CONFIG
  ]
};

const spanishConf = {
  module: COMMON_MODULE_CONFIG,
  output: {
    filename: 'spanish.js'
  },
  plugins: [
    COMMON_UGLIFY_CONFIG
  ]
};

module.exports = {
  commonConf:            commonConf,
  externalConf:          externalConf,
  modernConf:            modernConf,
  onDemandHeaderRawConf: onDemandHeaderRawConf,
  owningAHomeConf:       owningAHomeConf,
  spanishConf:           spanishConf
};
