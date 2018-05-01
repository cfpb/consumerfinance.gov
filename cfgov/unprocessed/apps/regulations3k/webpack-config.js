/* ==========================================================================
   Settings for webpack JavaScript bundling system.
   ========================================================================== */

const envVars = require( '../../../../config/environment' ).envvars;
const paths = require( '../../../../config/environment' ).paths;
const UglifyWebpackPlugin = require( 'uglifyjs-webpack-plugin' );
const fs = require( 'fs' );
const fancyLog = require( 'fancy-log' );
const swPrecache = require( 'sw-precache' );

// Constants
const APP_NAME = 'regulations3k';
// This'll need to be changed if the app doesn't live at cf.gov/regulations
const APP_PATH = 'regulations';
const SERVICE_WORKER_FILENAME = `${ APP_NAME }-service-worker.js`;
const SERVICE_WORKER_DEST = `cfgov/regulations3k/jinja2/regulations3k/${ SERVICE_WORKER_FILENAME }`;
const MANIFEST_FILENAME = `${ APP_NAME }-manifest.json`;
const MANIFEST_SRC = `${ paths.unprocessed }/apps/regulations3k/${ MANIFEST_FILENAME }`;
const MANIFEST_DEST = `${ paths.processed }/apps/regulations3k/${ MANIFEST_FILENAME }`;

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
  staticFileGlobs: [
    `${ paths.processed }/apps/regulations3k/css/main.css`,
    `${ paths.processed }/apps/regulations3k/js/index.js`
  ],
  stripPrefix: `${ paths.processed }/`,
  replacePrefix: /static/,
  runtimeCaching: [
    {
      urlPattern: new RegExp( `${ APP_PATH }` ),
      handler: 'fastest',
      options: {
        cache: {
          name: `${ APP_NAME }-content`,
          // Delete entries older than twelve hours
          maxAgeSeconds: 60 * 60 * 12
        }
      }
    },
    {
      urlPattern: new RegExp( `static/apps/${ APP_NAME }` ),
      handler: 'fastest',
      options: {
        cache: {
          name: `${ APP_NAME }-assets`,
          // Delete entries older than twelve hours
          maxAgeSeconds: 60 * 60 * 12
        }
      }
    },
    {
      urlPattern: new RegExp( 'static/(css|js|fonts|img)' ),
      handler: 'fastest',
      options: {
        cache: {
          name: 'cfpb-assets',
          // Delete entries older than twelve hours
          maxAgeSeconds: 60 * 60 * 12
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
    filename: '[name]',
    jsonpFunction: 'apps'
  },
  plugins: [
    COMMON_UGLIFY_CONFIG
  ],
  stats: STATS_CONFIG.stats
};

fancyLog( 'Started generating service worker file...' );
swPrecache.write( SERVICE_WORKER_DEST, SERVICE_WORKER_CONFIG, err => {
  if ( err ) {
    return fancyLog( `Error generating service worker file: ${ err }` );
  }
  return fancyLog( `Service worker file successfully generated to ${ SERVICE_WORKER_DEST }` );
} );

fancyLog( 'Copying eRegs\' manifest...' );
fs.copyFile( MANIFEST_SRC, MANIFEST_DEST, err => {
  if ( err ) {
    return fancyLog( `Error copying eRegs' manifest: ${ err }` );
  }
  return fancyLog( `Successfully copied eRegs' manifest to ${ SERVICE_WORKER_DEST }` );
} );

module.exports = { conf };
