/* eslint-disable complexity,consistent-return,global-require */
const copy = require( './copy.js' );
const scripts = require( './scripts.js' );
const styles = require( './styles.js' );

const { processed } = require( '../config/environment.js' ).paths;

const baseConfig = {
  logLevel: 'info',
  bundle: true,
  minify: true,
  sourcemap: true,
  external: [ '*.png', '*.woff', '*.woff2', '*.gif', '*.svg' ],
  outdir: `${ processed }`
};

const arg = process.argv.slice( 2 )[0];

( function() {
  if ( arg === 'copy' ) return copy( baseConfig );
  if ( arg === 'scripts' ) return scripts( baseConfig );
  if ( arg === 'styles' ) return styles( baseConfig );
  if ( arg === 'watch' ) baseConfig.watch = true;

  scripts( baseConfig );
  styles( baseConfig );
  copy( baseConfig );

  // Run app-specific scripts
  require( '../cfgov/unprocessed/apps/regulations3k/worker_and_manifest.js' );
} )();

