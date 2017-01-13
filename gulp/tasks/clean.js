'use strict';

var configClean = require( '../config' ).clean;
var del = require( 'del' );
var gulp = require( 'gulp' );

gulp.task( 'clean', function() {
  del( configClean.dest + '/**/*' );
} );
