'use strict';

var configScripts = require( '../config' ).scripts;
var fsHelper = require( '../utils/fs-helper' );
var globAll = require( 'glob-all' );
var gulp = require( 'gulp' );
var gulpUtil = require( 'gulp-util' );
var spawn = require( 'child_process' ).spawn;

// TODO: Update this to support grouping methods by class in the generated docs.
/**
 * Generate scripts documentation.
 */
function docsScripts() {
  globAll( configScripts.src, function( er, files ) {
    var options = [ 'build' ].concat( files ).concat(
                  [ '--github',
                    '--output=docs/scripts',
                    '--format=html' ] );
    spawn(
    fsHelper.getBinary( 'documentation', 'documentation.js' ),
      options, { stdio: 'inherit' }
    ).once( 'close', function() {
      gulpUtil.log( 'Scripts documentation generated!' );
    } );
  } );
}

gulp.task( 'docs:scripts', docsScripts );

gulp.task( 'docs',
  [
    'docs:scripts'
  ]
);
