const APP_NAME = 'mmt-my-money-calendar';
const PUBLIC_PATH = `/static/apps/${APP_NAME}/js/`;
const { paths } = require('../../../../config/environment');
const { LAST_2_IE_11_UP } = require('../../../../config/browser-list-config');
const webpack = require('webpack');
const path = require('path');
const TerserPlugin = require('terser-webpack-plugin');
const CopyPlugin = require('copy-webpack-plugin');
const WorkboxPlugin = require('workbox-webpack-plugin');
const { InjectManifest } = WorkboxPlugin;
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const OptimizeCssAssetsPlugin = require('optimize-css-assets-webpack-plugin');

// const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer');

// Used for toggling debug output. Inherit Django debug value to cut down on redundant environment variables:
const { DJANGO_DEBUG: DEBUG = false, NODE_ENV = 'development', ANALYZE = false } = process.env;

const COMMON_BUNDLE_NAME = 'common.js';
//const SERVICE_WORKER_DESTINATION = '../../../../jinja2/v1/mmt-my-money-calendar/service-worker.js';
const SERVICE_WORKER_DESTINATION = 'service-worker.js';

const AUTOLOAD_REACT = new webpack.ProvidePlugin({
  React: 'react',
});

const ENVIRONMENT_VARIABLES = new webpack.DefinePlugin({
  'process.env.NODE_ENV': JSON.stringify(NODE_ENV),
  'process.env.DEBUG': JSON.stringify(DEBUG),
});

const COPY_PWA_MANIFEST = new CopyPlugin([
  {
    from: path.join(__dirname, 'manifest.json'),
    to: '..',
  },
]);

const EXTRACT_CSS = new MiniCssExtractPlugin({
  moduleFilename: ({ name }) => `${name.replace('js', 'css')}`,
});

const GENERATE_SERVICE_WORKER = new InjectManifest({
  swSrc: 'cfgov/unprocessed/apps/mmt-my-money-calendar/js/sw.js',
  swDest: SERVICE_WORKER_DESTINATION,
});

const COMMON_MINIFICATION_CONFIG = [
  new TerserPlugin({
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
  }),
  new OptimizeCssAssetsPlugin(),
];

const COMMON_MODULE_CONFIG = {
  rules: [
    // Use Babel for JS and JSX
    {
      test: /\.jsx?$/,
      exclude: {
        test: /node_modules/,
        exclude: /node_modules\/(?:cf-.+|cfpb-.+)/,
      },
      use: {
        loader: 'babel-loader?cacheDirectory=true',
        options: {
          presets: [
            [
              '@babel/preset-env',
              {
                configPath: __dirname,
                useBuiltIns: DEBUG ? 'usage' : false,
                debug: DEBUG,
                targets: LAST_2_IE_11_UP,
              },
            ],
            [
              require('@babel/preset-react'),
              {
                development: NODE_ENV === 'development',
              },
            ],
          ],
          plugins: [
            [require('@babel/plugin-proposal-decorators'), { legacy: true }],
            [require('@babel/plugin-proposal-class-properties'), { loose: true }],
          ],
        },
      },
    },

    // Enable import and usage of images in bundle code
    {
      test: /\.(jpe?g|png|gif|svg)$/,
      use: ['file-loader'],
    },

    // Enable import of static CSS stylesheets
    {
      test: /\.css$/,
      use: [
        {
          loader: MiniCssExtractPlugin.loader,
          options: {
            publicPath: '/static/apps/mmt-my-money-calendar/js/',
          },
        },
        'css-loader',
      ],
    },

    // Allow font imports
    {
      test: /\.(woff2?|eot|ttf|otf)$/,
      use: ['file-loader'],
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

const plugins = [ENVIRONMENT_VARIABLES, AUTOLOAD_REACT, COPY_PWA_MANIFEST, EXTRACT_CSS, GENERATE_SERVICE_WORKER];

if (NODE_ENV === 'development') {
  if (ANALYZE) {
    const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer');

    plugins.push(
      new BundleAnalyzerPlugin({
        analyzerMode: 'server',
      })
    );
  }

  if (process.stdout.isTTY) {
    const ProgressBarPlugin = require('progress-bar-webpack-plugin');

    plugins.push(new ProgressBarPlugin());
  }
}

const conf = {
  cache: false,
  mode: NODE_ENV,
  module: COMMON_MODULE_CONFIG,
  output: {
    filename: '[name]',
    jsonpFunction: 'apps',
    publicPath: PUBLIC_PATH,
  },
  optimization: {
    minimize: NODE_ENV === 'production',
    minimizer: COMMON_MINIFICATION_CONFIG,
    /*
    runtimeChunk: true,
    splitChunks: {
      cacheGroups: {
        default: false,
        vendors: false,
        vendor: {
          chunks: 'all',
          test: /node_modules/,
        },
      },
    },
    */
  },
  stats: STATS_CONFIG.stats,
  devtool: NODE_ENV === 'production' ? false : 'inline-source-map',
  plugins,
};

module.exports = { conf };
