const gulp = require( 'gulp' );
const gulpUtil = require( 'gulp-util' );
const paths = require( '../../config/environment' ).paths;
const spawn = require( 'child_process' ).spawn;

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
