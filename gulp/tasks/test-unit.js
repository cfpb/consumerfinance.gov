const fancyLog = require( 'fancy-log' );
const fsHelper = require( '../utils/fs-helper' );
const gulp = require( 'gulp' );
const minimist = require( 'minimist' );
const spawn = require( 'child_process' ).spawn;
const paths = require( '../../config/environment' ).paths;

/**
 * Run JavaScript unit tests.
 * @param {Function} cb - Callback function to call on completion.
 */
function testUnitScripts( cb ) {
  const params = minimist( process.argv.slice( 3 ) ) || {};

  /* If --specs=path/to/js/spec flag is added on the command-line,
     pass the value to mocha to test individual unit test files. */
  let specs = params.specs;

  /* Set path defaults for source files.
     Remove ./ from beginning of path,
     which collectCoverageFrom doesn't support. */
  const pathSrc = paths.unprocessed.substring( 2 );

  // Set regex defaults.
  let fileTestRegex = 'unit_tests/';
  let fileSrcPath = pathSrc + '/';

  // If --specs flag is passed, adjust regex defaults.
  if ( specs ) {
    fileSrcPath += specs;
    // If the --specs argument is a file, strip it off.
    if ( specs.slice( -3 ) === '.js' ) {
      // TODO: Perform a more robust replacement here.
      fileSrcPath = fileSrcPath.replace( '-spec', '' );
      fileTestRegex += specs;
    } else {

      // Ensure there's a trailing slash.
      if ( specs.slice( -1 ) !== '/' ) {
        specs += '/';
      }

      fileSrcPath += '**/*.js';
      fileTestRegex += specs + '.*-spec.js';
    }
  } else {
    fileSrcPath += '**/*.js';
    fileTestRegex += '.*-spec.js';
  }

  /*
    The --no-cache flag is needed so the transforms don't cache.
    If they are cached, preprocessor-handlebars.js can't find handlebars. See
    https://facebook.github.io/jest/docs/en/troubleshooting.html#caching-issues
  */
  const jestOptions = [
    '--no-cache',
    '--config=jest.config.js',
    `--collectCoverageFrom=${ fileSrcPath }`,
    `--testRegex=${ fileTestRegex }`
  ];

  if ( params.ci ) {
    jestOptions.push( '--maxWorkers=2' );
  }

  spawn(
    fsHelper.getBinary( 'jest-cli', 'jest.js', '../bin' ),
    jestOptions,
    { stdio: 'inherit' }
  ).once( 'close', code => {
    if ( code ) {
      fancyLog( 'Unit tests exited with code ' + code );
      process.exit( 1 );
    }
    fancyLog( 'Unit tests done!' );
    cb();
  } );
}

gulp.task( 'test', testUnitScripts );
