'use strict';

var gulp = require( 'gulp' );
var gulpUtil = require( 'gulp-util' );
var paths = require( '../../config/environment' ).paths;
var spawn = require( 'child_process' ).spawn;

/**
 * Generate JS scripts documentation.
 */
function docsScripts() {
  spawn(
    paths.modules + '/.bin/jsdoc',
    [ paths.unprocessed + '/js',
      '--recurse',
      '--destination',
      './docs/scripts' ],
    { stdio: 'inherit' }
  ).once( 'close', function() {
    gulpUtil.log( 'Scripts documentation generated!' );
  } );
}

gulp.task( 'docs:scripts', docsScripts );

gulp.task( 'docs',
  [
    'docs:scripts'
  ]
);
