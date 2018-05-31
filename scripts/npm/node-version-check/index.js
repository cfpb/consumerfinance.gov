/*
This script requires a specific version of Node to be installed.
 */

const semver = require( 'semver' );

// The required version of Node is specified in package.json under `engines`
// eslint-disable-next-line no-process-env
const MIN_REQUIRED_VERSION = process.env.npm_package_engines_node;

if ( !semver.satisfies( process.version, MIN_REQUIRED_VERSION ) ) {
  throw new Error(
    `Node ${ MIN_REQUIRED_VERSION } or greater is required. ` +
    `You are running ${ process.version }.` +
    '\n'
  );
}
