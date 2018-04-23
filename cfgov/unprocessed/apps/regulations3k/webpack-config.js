/* ==========================================================================
   Settings for webpack JavaScript bundling system.
   ========================================================================== */


const BROWSER_LIST = require( '../../../../config/browser-list-config' );
const webpack = require( 'webpack' );
const UglifyWebpackPlugin = require( 'uglifyjs-webpack-plugin' );
const path = require( 'path' );
const SWPrecacheWebpackPlugin = require( 'sw-precache-webpack-plugin' );

// Constants
const COMMON_BUNDLE_NAME = 'common.js';
const SERVICE_WORKER_FILENAME = 'eregs-service-worker.js';
const SERVICE_WORKER_CACHEID = 'eregs';

/* Webpack plugin that generates a service worker using sw-precache that will
   cache webpack's bundles' emitted assets.
   https://github.com/goldhand/sw-precache-webpack-plugin */
const SERVICE_WORKERS_PRECACHE_CONFIG = new SWPrecacheWebpackPlugin( {
  cacheId: SERVICE_WORKER_CACHEID,
  filename: SERVICE_WORKER_FILENAME,
  minify: false,
  staticFileGlobs: [
    'static_built/apps/regulations3k/css/main.css',
    'static_built/apps/regulations3k/js/index.js'
  ],
  stripPrefix: 'static_built/',
  replacePrefix: /static/,
  runtimeCaching: [
    {
      urlPattern: '/eregulations3k\/(\\d\\d\\d\\d\/\\d)?/',
      handler: 'fastest',
      options: {
        cache: {
          maxEntries: 10,
          name: 'eregs-content'
        }
      }
    },
    {
      urlPattern: '/\/static\/app\/eregulations3k\/(css/js/img)\/.*\\.(css|js)/',
      handler: 'fastest',
      options: {
        cache: {
          maxEntries: 10,
          name: 'eregs-assets'
        }
      }
    }
  ]
} );

/* Set warnings to true to show linter-style warnings.
   Set mangle to false and beautify to true to debug the output code. */
const COMMON_UGLIFY_CONFIG = new UglifyWebpackPlugin( {
  cache: true,
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

/* Commmon webpack 'module' option used in each configuration.
   Runs code through Babel and uses global supported browser list. */
const COMMON_MODULE_CONFIG = {
  rules: [ {
    test: /\.js$/,

    /* The below regex will capture all node modules that start with `cf`
      or atomic-component. Regex test: https://regex101.com/r/zizz3V/1/. */
    exclude: /node_modules\/(?:cf.+|atomic-component)/,
    use: {
      loader: 'babel-loader?cacheDirectory=true',
      options: {
        presets: [ [ 'babel-preset-env', {
          targets: {
            browsers: BROWSER_LIST.LAST_2_IE_9_UP
          },
          debug: true
        } ] ]
      }
    }
  } ]
};

const COMMON_CHUNK_CONFIG = new webpack.optimize.SplitChunksPlugin( {
  name: COMMON_BUNDLE_NAME
} );

const STATS_CONFIG = {
  stats: {
    entrypoints: false
  }
};

const conf = {
  cache: false,
  module: COMMON_MODULE_CONFIG,
  mode: 'production',
  output: {
    filename: '[name]',
    jsonpFunction: 'apps'
  },
  plugins: [
    COMMON_CHUNK_CONFIG,
    COMMON_UGLIFY_CONFIG,
    SERVICE_WORKERS_PRECACHE_CONFIG
  ],
  stats: STATS_CONFIG.stats
};

module.exports = { conf };
