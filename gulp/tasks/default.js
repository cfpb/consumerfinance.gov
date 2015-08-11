'use strict';

var gulp = require( 'gulp' );

gulp.task( 'default',
  [
    'lint:src',
    'test:unit',
    'test:macro',
    'test:processor',
    'build'
  ]
);
