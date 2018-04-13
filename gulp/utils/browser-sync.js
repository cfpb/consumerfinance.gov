const envvars = require( '../../config/environment' ).envvars;
const through2 = require( 'through2' );

/**
 * The browser-sync dependency is required inside this function so that
 * it can be kept in devDependencies instead of dependencies.
 * @returns {*} Empty stream or stream from browser-sync.
 */
function runBrowserSyncApp() {
  if ( envvars.NODE_ENV === 'production' ) { return through2.obj(); }

  // eslint-disable-next-line global-require
  const browserSync = require( 'browser-sync' );
  return browserSync.reload( { stream: true } );
}

module.exports = { runBrowserSyncApp };
