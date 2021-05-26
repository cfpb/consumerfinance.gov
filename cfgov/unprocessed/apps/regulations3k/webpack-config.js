/* ==========================================================================
   Settings for webpack JavaScript bundling system.
   ========================================================================== */

const paths = require( '../../../../config/environment' ).paths;
const TerserPlugin = require( 'terser-webpack-plugin' );
const fs = require( 'fs' );
const path = require( 'path' );
const fancyLog = require( 'fancy-log' );
const workboxBuild = require( 'workbox-build' );

// Constants
const APP_NAME = 'regulations3k';
// This'll need to be changed if the app doesn't live at cf.gov/regulations
const APP_PATH = 'policy-compliance/rulemaking/regulations';
const SERVICE_WORKER_FILENAME = `${ APP_NAME }-service-worker.js`;
const SERVICE_WORKER_DEST = `cfgov/${ APP_NAME }/jinja2/${ APP_NAME }/${ SERVICE_WORKER_FILENAME }`;
const MANIFEST_FILENAME = `${ APP_NAME }-manifest.json`;
const MANIFEST_SRC = `${ paths.unprocessed }/apps/${ APP_NAME }/${ MANIFEST_FILENAME }`;
const MANIFEST_DEST = `${ paths.processed }/apps/${ APP_NAME }/${ MANIFEST_FILENAME }`;

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

const SERVICE_WORKER_CONFIG = {
  swDest: SERVICE_WORKER_DEST,
  globDirectory: paths.processed,
  globPatterns: [
    `apps/${ APP_NAME }/css/main.css`,
    `apps/${ APP_NAME }/js/index.js`
  ],
  modifyURLPrefix: {
    'apps/': '/static/apps/'
  },
  runtimeCaching: [
    {
      urlPattern: new RegExp( `/${ APP_PATH }/` ),
      handler: 'StaleWhileRevalidate',
      options: {
        cacheName: `${ APP_NAME }-content`,
        expiration: {
          maxAgeSeconds: 60 * 60 * 3
        }
      }
    },
    {
      urlPattern: new RegExp( `/static/apps/${ APP_NAME }` ),
      handler: 'StaleWhileRevalidate',
      options: {
        cacheName: `${ APP_NAME }-assets`,
        expiration: {
          maxAgeSeconds: 60 * 60 * 3
        }
      }
    },
    {
      urlPattern: new RegExp( '/static/(css|js|fonts|img)' ),
      handler: 'StaleWhileRevalidate',
      options: {
        cacheName: 'cfpb-assets',
        expiration: {
          maxAgeSeconds: 60 * 60 * 3
        }
      }
    }
  ]
};

const conf = {
  cache: false,
  module: COMMON_MODULE_CONFIG,
  mode: 'production',
  output: {
    filename: '[name]'
  },
  optimization: {
    minimize: true,
    minimizer: [
      COMMON_MINIFICATION_CONFIG
    ]
  },
  resolve: {
    symlinks: false
  },
  stats: STATS_CONFIG.stats
};

const ensureDirectoryExistence = filePath => {
  const dirname = path.dirname( filePath );
  if ( fs.existsSync( dirname ) ) { // eslint-disable-line no-sync
    return true;
  }
  ensureDirectoryExistence( dirname );
  return fs.mkdirSync( dirname ); // eslint-disable-line no-sync
};

fancyLog( 'Started generating service worker file...' );
ensureDirectoryExistence( SERVICE_WORKER_DEST );
workboxBuild.generateSW( SERVICE_WORKER_CONFIG ).then( ( { count, size } ) => {
  fancyLog( `Generated ${ SERVICE_WORKER_DEST }, which will precache ${ count } files, totaling ${ size } bytes.` );
} ).catch( err => {
  fancyLog( `Error generating service worker file: ${ err }` );
} );

fancyLog( 'Copying eRegs\' manifest...' );
ensureDirectoryExistence( MANIFEST_DEST );
fs.copyFile( MANIFEST_SRC, MANIFEST_DEST, err => {
  if ( err ) {
    return fancyLog( `Error copying eRegs' manifest: ${ err }` );
  }
  return fancyLog( `Successfully copied eRegs' manifest to ${ MANIFEST_DEST }` );
} );

module.exports = { conf };
