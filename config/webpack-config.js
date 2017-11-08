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


const STATS = {
  // Add chunk information (setting this to `false` allows for a less verbose output)
  chunks: true,
  // Add built modules information to chunk information
  chunkModules: true,
  // Add the origins of chunks and chunk merging info
  chunkOrigins: true,
  // Add errors
  errors: true,
  // Add timing information
  timings: true
};

// Commmon webpack 'module' option used in each configuration.
// Runs code through Babel and uses global supported browser list.
const COMMON_MODULE = {
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
const COMMON_UGLIFY = new UglifyWebpackPlugin( {
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

const MODERN = {
  cache: true,
  profile: true,
  context: path.join( __dirname, '/../', paths.unprocessed, JS_ROUTES_PATH ),
  entry: scriptsManifest.getDirectoryMap( paths.unprocessed + JS_ROUTES_PATH ),
  module: COMMON_MODULE,
  output: {
    path: path.join( __dirname, 'js' ),
    filename: '[name]'
  },
  plugins: [
    new webpack.optimize.CommonsChunkPlugin( {
      name: COMMON_BUNDLE_NAME
    } ),
    COMMON_UGLIFY
  ]
};

const IE = {
  entry: paths.unprocessed + '/js/ie/common.ie.js',
  module: COMMON_MODULE,
  output: {
    filename: 'common.ie.js'
  },
  plugins: [ COMMON_UGLIFY ]
};

const EXTERNAL = {
  entry: paths.unprocessed + JS_ROUTES_PATH + '/external-site/index.js',
  module: COMMON_MODULE,
  output: {
    filename: 'external-site.js'
  },
  plugins: [ COMMON_UGLIFY ]
};

const ON_DEMAND = {
  context: path.join( __dirname, '/../', paths.unprocessed,
                      JS_ROUTES_PATH + '/on-demand' ),
  entry:   scriptsManifest.getDirectoryMap( paths.unprocessed +
                                            JS_ROUTES_PATH + '/on-demand' ),
  module: COMMON_MODULE,
  output: {
    path:     path.join( __dirname, 'js' ),
    filename: '[name]'
  },
  plugins: [ COMMON_UGLIFY ]
};

const ON_DEMAND_HEADER_RAW = {
  context: path.join( __dirname, '/../', paths.unprocessed,
                      JS_ROUTES_PATH + '/on-demand' ),
  entry:  './header.js',
  module: COMMON_MODULE,
  output: {
    path:     path.join( __dirname, 'js' ),
    filename: '[name]'
  }
};

const SPANISH = {
  entry: paths.unprocessed +
         JS_ROUTES_PATH + '/es/obtener-respuestas/single.js',
  module: COMMON_MODULE,
  output: {
    filename: 'spanish.js'
  },
  plugins: [ COMMON_UGLIFY ]
};

const OWNING_A_HOME = {
  cache: true,
  context: path.join( __dirname, '/../',
    paths.unprocessed, OAH_COMMON_BUNDLE_ROUTE
  ),
  entry: scriptsManifest.getDirectoryMap(
    paths.unprocessed + OAH_COMMON_BUNDLE_ROUTE
  ),
  module: COMMON_MODULE,
  output: {
    path: path.join( __dirname, 'js' ),
    filename: '[name]',
    jsonpFunction: 'OAH'
  },
  plugins: [
    new webpack.optimize.CommonsChunkPlugin( {
      name: COMMON_BUNDLE_NAME
    } ),
    COMMON_UGLIFY ]
};

module.exports = {
  EXTERNAL,
  IE,
  MODERN,
  ON_DEMAND,
  ON_DEMAND_HEADER_RAW,
  OWNING_A_HOME,
  SPANISH,
  STATS
};
