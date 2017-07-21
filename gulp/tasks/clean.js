'use strict';

const configClean = require( '../config' ).clean;
const del = require( 'del' );
const gulp = require( 'gulp' );

gulp.task( 'clean', () => {
  del( configClean.dest + '/**/*' );
} );
