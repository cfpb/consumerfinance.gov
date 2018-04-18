const del = require( 'del' );
const gulp = require( 'gulp' );
const paths = require( '../../config/environment' ).paths;

// Clean CSS out of /cfgov/static_built/css/
gulp.task( 'clean:css', () => del( [
  paths.processed + '/css/**/*',
  paths.processed + '/apps/**/css/*'
] ) );

// Clean JavaScript out of /cfgov/static_built/js/
gulp.task( 'clean:js', () => del( [
  paths.processed + '/js/**/*',
  paths.processed + '/apps/**/js/*'
] ) );

// Clean everything out of /cfgov/static_built/
gulp.task( 'clean', () => del( paths.processed + '/**/*' ) );
