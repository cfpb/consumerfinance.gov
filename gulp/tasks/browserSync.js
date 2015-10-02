'use strict';

var gulp = require( 'gulp' );
var util = require( 'gulp-util' );
var browserSync = require( 'browser-sync' );

gulp.task( 'browserSync', function() {
  var port = util.env.port || process.env.HTTP_PORT || '8000'; // eslint-disable-line no-process-env, no-inline-comments, max-len
  browserSync.init( {
    //proxy: 'localhost:' + port
  } );
} );
