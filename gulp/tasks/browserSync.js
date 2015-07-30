'use strict';

var gulp = require( 'gulp' );
var util = require( 'gulp-util' );
var browserSync = require( 'browser-sync' );

gulp.task( 'browserSync', function() {
  var port = util.env.port || '7000';
  browserSync.init( {
    proxy: 'localhost:' + port
  } );
} );
