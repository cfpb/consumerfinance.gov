const { LAST_2_IE_11_UP } = require('../../../../config/browser-list-config');
const webpack = require('webpack');
const TerserPlugin = require('terser-webpack-plugin');
const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer');

const reactPreset = require('@babel/preset-react');
const classPropertiesPlugin = require('@babel/plugin-proposal-class-properties');

// Used for toggling debug output. Inherit Django debug value to cut down on redundant environment variables:
const {
  DJANGO_DEBUG: DEBUG = false,
  NODE_ENV = 'development',
  ANALYZE = false,
} = process.env;

const COMMON_BUNDLE_NAME = 'common.js';

const AUTOLOAD_REACT = new webpack.ProvidePlugin({
  React: 'react',
});

const COMMON_MINIFICATION_CONFIG = new TerserPlugin({
  cache: true,
  parallel: true,
  extractComments: true,
  terserOptions: {
    ie8: false,
    ecma: 5,
    warnings: false,
    mangle: true,
    output: {
      comments: false,
      beautify: false,
    },
  },
});

const COMMON_MODULE_CONFIG = {
  rules: [
    {
      test: /\.js$/,
      exclude: {
        test: /node_modules/,
        exclude: /node_modules\/(?:cf-.+|cfpb-.+)/,
      },
      use: {
        loader: 'babel-loader?cacheDirectory=true',
        options: {
          presets: [
            ['@babel/preset-env', {
              configPath: __dirname,
              useBuiltIns: DEBUG ? 'usage' : false,
              debug: DEBUG,
              targets: LAST_2_IE_11_UP,
            }],
            [reactPreset, {
              development: NODE_ENV === 'development',
            }],
          ],
          plugins: [
            [classPropertiesPlugin, {
              loose: true,
            }],
          ],
        },
      },
    },
  ],
};

const STATS_CONFIG = {
  stats: {
    entrypoints: false,
  },
};

/**
 * TODO: Set up service worker config using workbox for offline capability
 */

const plugins = [
  AUTOLOAD_REACT,
];

if (NODE_ENV === 'development' && ANALYZE) {
  plugins.push(new BundleAnalyzerPlugin({
    analyzerMode: 'server',
  }));
}

const conf = {
  cache: false,
  mode: NODE_ENV,
  module: COMMON_MODULE_CONFIG,
  output: {
    filename: '[name]',
    jsonpFunction: 'apps',
  },
  optimization: {
    minimize: true,
    minimizer: [
      COMMON_MINIFICATION_CONFIG,
    ],
  },
  stats: STATS_CONFIG.stats,
  devtool: NODE_ENV === 'production' ? false : 'inline-source-map',
  plugins,
};

module.exports = { conf };
