const browserSync = require( 'browser-sync' );
const envvars = require( '../../config/environment' ).envvars;
const gulp = require( 'gulp' );

gulp.task( 'browsersync', () => {
  const host = envvars.TEST_HTTP_HOST;
  const port = envvars.TEST_HTTP_PORT;
  browserSync.init( {
    proxy: host + ':' + port
  } );
} );
