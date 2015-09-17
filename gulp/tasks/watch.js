'use strict';

/* Notes:
   - gulp/tasks/scripts.js handles js recompiling with webpack --watch flag.
   - gulp/tasks/browserSync.js watches and reloads compiled files.
*/

var gulp = require( 'gulp' );
var config = require( '../config' );
var scripts = require( './scripts' );

gulp.task( 'watch', [ 'browserSync' ], function() {
  scripts.webpackTask( true );
  gulp.watch( config.styles.cwd + '/**/*.less', [ 'styles' ] );
  gulp.watch( config.images.src, [ 'images' ] );
  gulp.watch( config.copy.files.src, [ 'copy:files' ] );
} );
