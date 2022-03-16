/* gulpfile.js
   ===========
   Rather than manage one giant configuration file responsible
   for creating multiple tasks, each task has been broken out into
   its own file in gulp/tasks. Any files in that directory get
   automatically required below.
   To add a new task, simply add a new task file the gulp/tasks directory.
 */

const fancyLog = require( 'fancy-log' );
const fs = require( 'fs' );
const glob = require( 'glob' );
const gulp = require( 'gulp' );
const path = require( 'path' );

const TASK_PATH = './gulp/tasks/';

/**
 * Require a gulp task and log the task to the console.
 * @param  {string} taskPath - Path to a gulp task.
 */
function requireTask( taskPath ) {
  fancyLog( 'Requiring task', taskPath );
  // eslint-disable-next-line global-require
  require( path.resolve( taskPath ) );
}

/**
 * Recursively check that a file exists on disk, given a file pattern in the
 * format file-name.
 * E.g. Take the file pattern test-unit-scripts.
 * This function will check (recursively)
 * whether test-unit-scripts, test-unit, and test exist.
 * If one of those exist, it will return the first occurence,
 * otherwise it will return undefined.
 * @param  {string} filePattern A filename pattern in the format file-name.
 * @returns {string|undefined} File name that exists, otherwise undefined.
 */
function fileExists( filePattern ) {
  if ( !filePattern ) {
    let UNDEFINED;
    return UNDEFINED;
  }
  const checkFile = `${ TASK_PATH }${ filePattern }.js`;
  // eslint-disable-next-line no-sync
  if ( fs.existsSync( checkFile ) ) {
    return checkFile;
  }
  const newFile = filePattern.split( '-' );
  newFile.pop();
  return fileExists( newFile.join( '-' ) );
}

/**
 * Load the default set of gulp tasks.
 */
function requireAllDefaultTasks() {
  // Automatically add tasks in the /tasks/ directory.
  glob.sync( `${ TASK_PATH }*.js` ).forEach( task => {
    requireTask( task );
  } );

  // Define top-level tasks.
  gulp.task( 'build',
    gulp.series(
      gulp.parallel(
        'styles',
        'scripts',
        'images'
      ),
      'copy'
    )
  );

  // Define the task that runs with `gulp watch`.
  gulp.task( 'watch',
    gulp.parallel(
      'styles:watch',
      'scripts:watch'
    )
  );

  // Define the default task that runs with just `gulp`.
  gulp.task( 'default',
    gulp.parallel(
      'build'
    )
  );
}

/*
Check for command-line flag option (such as `styles` in `gulp styles`).
If the option maps to a task in /gulp/tasks/, we can skip loading other tasks.
*/
const cliOption = process.argv.slice( 2 );
let taskName;
if ( cliOption.length > 0 ) {
  taskName = cliOption[0].replace( /:/g, '-' );
}
const taskFile = fileExists( taskName );

if ( taskFile ) {
  requireTask( taskFile );
} else {
  requireAllDefaultTasks();
}
