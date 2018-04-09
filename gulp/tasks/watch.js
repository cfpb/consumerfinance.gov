/* Notes:
   - gulp/tasks/browserSync.js watches and reloads compiled files. */
const fancyLog = require( 'fancy-log' );
const gulp = require( 'gulp' );
const paths = require( '../../config/environment' ).paths;

/**
 * Add reporting output to watched files.
 * @param {FSWatcher} watcher - Output from gulp.watch.
 */
function _addChangeListener( watcher ) {
  watcher.on( 'change', function( path, stats ) {
    fancyLog.info( 'File ' + path + ' was changed' );
  } );

  watcher.on('unlink', function( path ) {
    fancyLog.info( 'File ' + path + ' was removed' );
  } );
}

gulp.task( 'watch',
  gulp.parallel( 'browsersync', () => {
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
  } )
);
