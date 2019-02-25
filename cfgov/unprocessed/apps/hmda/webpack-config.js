/* ==========================================================================
   Settings for webpack JavaScript bundling system.
   ========================================================================== */

const UglifyWebpackPlugin = require( 'uglifyjs-webpack-plugin' );

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
    use: {
      loader: 'babel-loader?cacheDirectory=true',
      options: {
        presets: [ [ '@babel/preset-env', {
          configPath: __dirname,

          /* Use useBuiltIns: 'usage' and set `debug: true` to see what
             scripts require polyfilling. */
          useBuiltIns: false,
          debug: false
        } ] ]
      }
    }
  } ]
};

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
    COMMON_UGLIFY_CONFIG
  ],
  resolve: {
    symlinks: false
  },
  stats: STATS_CONFIG.stats
};

module.exports = { conf };
