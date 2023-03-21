/*
This script handles installing node dependencies for a project that lives
under consumerfinance.gov, but has its own package.json. These projects appear
under the ./cfgov/unprocessed/apps/ path.
 */

import * as fs from 'fs';
import childProcess from 'child_process';
const execSync = childProcess.execSync;

import environment from '../../../config/environment.js';
const paths = environment.paths;

// Aggregate application namespaces that appear in unprocessed/apps.
let apps = fs.readdirSync(`${paths.unprocessed}/apps/`);

// Filter out hidden directories.
apps = apps.filter((dir) => dir.charAt(0) !== '.');

// Install each application's dependencies.
apps.forEach((app) => {
  /* Check if package.json exists in a particular app's folder.
     If it does, run yarn install on that directory. */
  const appsPath = `${paths.unprocessed}/apps/${app}`;
  const pkgPath = `${appsPath}/package.json`;

  if (fs.existsSync(pkgPath)) {
    const pkgJSON = JSON.parse(fs.readFileSync(pkgPath));
    if (
      (pkgJSON.dependencies &&
        Object.keys(pkgJSON.dependencies).length !== 0) ||
      (pkgJSON.devDependencies &&
        Object.keys(pkgJSON.devDependencies).length !== 0)
    ) {
      try {
        const stdOut = execSync(`yarn --cwd ${appsPath} install`);
        // eslint-disable-next-line no-console
        console.log(`${appsPath}'s yarn output: ${stdOut.toString()}`);
      } catch (error) {
        if (error.stderr) {
          // eslint-disable-next-line no-console
          console.log(`yarn output from ${appsPath}: ${error.stderr}`);
        }

        // eslint-disable-next-line no-console
        console.log(`exec error from ${appsPath}: ${error}`);
        process.exit(1);
      }
    }
  }
});
