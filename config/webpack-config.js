/* ==========================================================================
   Settings for webpack JavaScript bundling system.
   ========================================================================== */

const envvars = require( '../config/environment' ).envvars;
const webpack = require( 'webpack' );
const TerserPlugin = require( 'terser-webpack-plugin' );

// Constants
const COMMON_BUNDLE_NAME = 'common.js';

/* This sets the default mode for webpack configurations to satisfy the need
   of webpack to have a `mode` set.
   This value gets overridden when NODE_ENV=development.
   See the `if ( envvars.NODE_ENV === 'development' )` block below. */
const WEBPACK_MODE_DEFAULT = 'production';

/* Commmon webpack 'module' option used in each configuration.
   Runs code through Babel and uses global supported browser list. */
const COMMON_MODULE_CONFIG = {
  rules: [ {
    test: /\.js$/,

    /* Exclude modules from transpiling.
       The below regex will match and exclude all node modules
       except those that start with `@cfpb/` or `cfpb-`.
       Regex test: https://regex101.com/r/zizz3V/9 */
    exclude: /node_modules\/(?!(?:@cfpb\/.+|cfpb\-.+)).+/,
    use: {
      loader: 'babel-loader?cacheDirectory=true',
      options: {
        presets: [ [ '@babel/preset-env', {

          /* Use useBuiltIns: 'usage' and set `debug: true` to see what
             scripts require polyfilling. */
          useBuiltIns: false,
          debug: false
        } ] ]
      }
    }
  },
  {
    test: /\.svg$/,
    loader: 'svg-inline-loader'
  } ]
};

/* Set warnings to true to show linter-style warnings.
   Set mangle to false and beautify to true to debug the output code. */
const COMMON_MINIFICATION_CONFIG = new TerserPlugin( {
  parallel: true,
  extractComments: false,
  terserOptions: {
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

const COMMON_CHUNK_CONFIG = new webpack.optimize.SplitChunksPlugin( {
  name: COMMON_BUNDLE_NAME
} );

const STATS_CONFIG = {
  stats: {
    entrypoints: false
  }
};

const commonConf = {
  cache: true,
  mode: WEBPACK_MODE_DEFAULT,
  module: COMMON_MODULE_CONFIG,
  output: {
    filename: '[name]'
  },
  optimization: {
    minimizer: [
      COMMON_MINIFICATION_CONFIG
    ]
  },
  resolve: {
    symlinks: false
  },
  stats: STATS_CONFIG.stats
};

const modernConf = {
  cache: true,
  mode: WEBPACK_MODE_DEFAULT,
  module: COMMON_MODULE_CONFIG,
  output: {
    filename: '[name]'
  },
  plugins: [
    COMMON_CHUNK_CONFIG
  ],
  optimization: {
    minimizer: [
      COMMON_MINIFICATION_CONFIG
    ]
  },
  resolve: {
    symlinks: false
  },
  stats: STATS_CONFIG.stats
};

const onDemandHeaderRawConf = {
  mode: WEBPACK_MODE_DEFAULT,
  module: COMMON_MODULE_CONFIG,
  resolve: {
    symlinks: false
  }
};

const appsConf = {
  cache: true,
  mode: WEBPACK_MODE_DEFAULT,
  module: COMMON_MODULE_CONFIG,
  output: {
    filename: '[name]'
  },
  plugins: [
    COMMON_CHUNK_CONFIG
  ],
  optimization: {
    minimizer: [
      COMMON_MINIFICATION_CONFIG
    ]
  },
  resolve: {
    symlinks: false
  },
  stats: STATS_CONFIG.stats
};

const spanishConf = {
  cache: true,
  mode: WEBPACK_MODE_DEFAULT,
  module: COMMON_MODULE_CONFIG,
  output: {
    filename: 'spanish.js'
  },
  optimization: {
    minimizer: [
      COMMON_MINIFICATION_CONFIG
    ]
  },
  resolve: {
    symlinks: false
  },
  stats: STATS_CONFIG.stats
};

const devConf = {
  devtool: 'inline-source-map',
  mode: 'development',
  module: COMMON_MODULE_CONFIG,
  plugins: [],
  resolve: {
    symlinks: false
  }
};

const configExports = {
  commonConf,
  devConf,
  modernConf,
  onDemandHeaderRawConf,
  appsConf,
  spanishConf
};

if ( envvars.NODE_ENV === 'development' ) {
  // eslint-disable-next-line guard-for-in
  let key;
  for ( key in configExports ) {
    if ( {}.hasOwnProperty.call( configExports, key ) ) {
      Object.assign( configExports[key], devConf );
    }
  }
}

module.exports = configExports;
