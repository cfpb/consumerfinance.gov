/* Notes:
   - gulp/tasks/browserSync.js watches and reloads compiled files. */

const gulp = require( 'gulp' );
const config = require( '../config' );

gulp.task( 'watch', [ 'browsersync' ], function() {
  gulp.watch( config.scripts.src, [ 'scripts' ] );
  gulp.watch( [ config.styles.cwd + '/**/*.less', config.legacy.cwd + '/*/less/*.less' ], [ 'styles' ] );
} );

