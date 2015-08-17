'use strict';

var gulp = require( 'gulp' );

gulp.task( 'default',
  [
    'lint:scripts',
    'test:unit',
    'build'
  ]
);
