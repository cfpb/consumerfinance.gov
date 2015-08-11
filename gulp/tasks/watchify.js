'use strict';

var gulp = require( 'gulp' );
var scriptsTask = require( './scripts' );

gulp.task( 'watchify', function() {
  // Start browserify task with devMode === true
  return scriptsTask( true );
} );
