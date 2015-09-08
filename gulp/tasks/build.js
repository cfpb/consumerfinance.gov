'use strict';

var gulp = require( 'gulp' );

gulp.task( 'build',
  [
    'styles',
    'ieStyles',
    'scripts',
    'images',
    'copy'
  ]
);
