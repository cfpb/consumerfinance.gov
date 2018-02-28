/*
This script handles installing node dependencies for a project that lives
under cfgov-refresh, but has its own package.json. These projects appear
under the ./cfgov/unprocessed/apps/ path.
 */

const fs = require( 'fs' );
const exec = require( 'child_process' ).exec;

const paths = require( '../../../config/environment' ).paths;

// Aggregate application namespaces that appear in unprocessed/apps.
// eslint-disable-next-line no-sync
let apps = fs.readdirSync( `${ paths.unprocessed }/apps/` );

// Filter out .DS_STORE directory.
apps = apps.filter( dir => dir.charAt( 0 ) !== '.' );

// Run each application's JS through webpack and store the gulp streams.
apps.forEach( app => {
  /* Check if node_modules directory exists in a particular app's folder.
     If it doesn't log the command to add it and don't process the scripts. */
  const appsPath = `${ paths.unprocessed }/apps/${ app }`;
  // eslint-disable-next-line no-sync
  if ( fs.existsSync( `${ appsPath }/package.json` ) ) {
    exec( `npm --prefix ${ appsPath } install ${ appsPath }`,
      ( error, stdout, stderr ) => {
        // eslint-disable-next-line no-console
        console.log( 'App\'s npm output: ' + stdout );
        // eslint-disable-next-line no-console
        console.log( 'App\'s npm errors: ' + stderr );
        if ( error !== null ) {
          // eslint-disable-next-line no-console
          console.log( 'App\'s exec error: ' + error );
        }
      }
    );
  }
} );
