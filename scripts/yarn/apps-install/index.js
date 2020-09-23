/*
This script handles installing node dependencies for a project that lives
under consumerfinance.gov, but has its own package.json. These projects appear
under the ./cfgov/unprocessed/apps/ path.
 */

const fs = require( 'fs' );
// eslint-disable-next-line no-sync
const execSync = require( 'child_process' ).execSync;

const paths = require( '../../../config/environment' ).paths;

// Aggregate application namespaces that appear in unprocessed/apps.
// eslint-disable-next-line no-sync
let apps = fs.readdirSync( `${ paths.unprocessed }/apps/` );

// Filter out hidden directories.
apps = apps.filter( dir => dir.charAt( 0 ) !== '.' );

// Install each application's dependencies.
apps.forEach( app => {
  /* Check if package.json exists in a particular app's folder.
     If it does, run yarn install on that directory. */
  const appsPath = `${ paths.unprocessed }/apps/${ app }`;
  const pkgPath = `${ appsPath }/package.json`;

  // eslint-disable-next-line no-sync
  if ( fs.existsSync( pkgPath ) ) {
    // eslint-disable-next-line no-sync
    const pkgJSON = JSON.parse( fs.readFileSync( pkgPath ) );
    if (
      ( pkgJSON.dependencies &&
        Object.keys( pkgJSON.dependencies ).length !== 0
      ) || (
        pkgJSON.devDependencies &&
        Object.keys( pkgJSON.devDependencies ).length !== 0
      )
    ) {
      try {
        // eslint-disable-next-line no-sync
        const stdOut = execSync(
          `yarn --cwd ${ appsPath } install`
        );
        // eslint-disable-next-line no-console
        console.log( `${ appsPath }'s yarn output: ${ stdOut.toString() }` );
      } catch ( error ) {
        if ( error.stderr ) {
          // eslint-disable-next-line no-console
          console.log( `yarn output from ${ appsPath }: ${ error.stderr }` );
        }

        // eslint-disable-next-line no-console
        console.log( `exec error from ${ appsPath }: ${ error }` );
        // eslint-disable-next-line no-process-exit
        process.exit( 1 );
      }
    }
  }
} );
