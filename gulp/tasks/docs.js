const fancyLog = require( 'fancy-log' );
const gulp = require( 'gulp' );
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
    fancyLog( 'Scripts documentation generated!' );
  } );
}

gulp.task( 'docs:scripts', docsScripts );

gulp.task( 'docs',
  gulp.parallel(
    'docs:scripts'
  )
);
