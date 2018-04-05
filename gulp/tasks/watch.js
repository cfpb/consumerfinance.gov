/* Notes:
   - gulp/tasks/browserSync.js watches and reloads compiled files. */

const gulp = require( 'gulp' );
const config = require( '../config' );
const paths = require( '../../config/environment' ).paths;

gulp.task( 'watch',
  gulp.series( 'browsersync', () => {
    gulp.watch( [
      config.scripts.src,
      paths.unprocessed + '/apps/**/js/**/*.js'
    ], [ 'scripts' ] );
    gulp.watch( [
      config.styles.cwd + '/**/*.less',
      config.legacy.cwd + '/*/less/*.less',
      paths.unprocessed + '/apps/**/css/**/*.less'
    ], [ 'styles' ] );
  } )
);
