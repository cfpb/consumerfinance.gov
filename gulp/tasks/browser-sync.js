'use strict';

var browserSync = require( 'browser-sync' );
var envvars = require( '../../config/environment' ).envvars;
var gulp = require( 'gulp' );

gulp.task( 'browsersync', function() {
  var host = envvars.TEST_HTTP_HOST;
  var port = envvars.TEST_HTTP_PORT;
  browserSync.init( {
    proxy: host + ':' + port
  } );
} );
