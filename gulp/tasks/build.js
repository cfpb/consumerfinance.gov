const gulp = require( 'gulp' );

gulp.task( 'build',
  [
    'styles',
    'scripts',
    'images',
    'copy'
  ]
);
