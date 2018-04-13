/* Notes:
   - gulp/tasks/browserSync.js watches and reloads compiled files. */
const envvars = require( '../../config/environment' ).envvars;
const fancyLog = require( 'fancy-log' );
const gulp = require( 'gulp' );
const paths = require( '../../config/environment' ).paths;
const through2 = require( 'through2' );

/**
 * Add reporting output to watched files.
 * @param {FSWatcher} watcher - Output from gulp.watch.
 */
function _addChangeListener( watcher ) {
  watcher.on(
    'change',
    path => fancyLog.info( 'File ' + path + ' was changed' )
  );

  watcher.on(
    'unlink',
    path => fancyLog.info( 'File ' + path + ' was removed' )
  );
}

/**
 * Run browsersync watch task.
 * @returns {PassThrough} A source stream.
 */
function taskWatch() {
  return gulp.parallel( 'browsersync', () => {
    const jsWatcher = gulp.watch( [
      paths.unprocessed + '/js/**/*.js',
      paths.unprocessed + '/apps/**/js/**/*.js'
    ], gulp.parallel( 'scripts' ) );
    _addChangeListener( jsWatcher );

    const cssWatcher = gulp.watch( [
      paths.unprocessed + '/css/**/*.less',
      paths.unprocessed + '/apps/**/css/**/*.less',
      paths.legacy + '/*/less/*.less'
    ], gulp.parallel( 'styles' ) );
    _addChangeListener( cssWatcher );
  } );
}

/**
 * @param {Function} cb callback function of gulp task.
 * @returns {*} Result of gulp callback.
 */
function taskWatchNotSupported( cb ) {
  fancyLog.warn( 'NODE_ENV in production, \'watch\' task not supported!' );
  return cb();
}

/**
 * Run browserSync task.
 * The browser-sync dependency is required in this function so that
 * it can be kept in devDependencies instead of dependencies.
 */
gulp.task( 'browsersync', () => {
  // eslint-disable-next-line global-require
  const browserSync = require( 'browser-sync' );

  const host = envvars.TEST_HTTP_HOST;
  const port = envvars.TEST_HTTP_PORT;
  browserSync.init( {
    proxy: host + ':' + port
  } );
} );

gulp.task(
  'watch',
  envvars.NODE_ENV === 'production' ? taskWatchNotSupported : taskWatch()
);
