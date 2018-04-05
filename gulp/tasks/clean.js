const del = require( 'del' );
const gulp = require( 'gulp' );
const paths = require( '../../config/environment' ).paths;

// Clean CSS out of /cfgov/static_built/css/
gulp.task( 'clean:css', cb => {
  del( paths.processed + '/css/**/*' );
  del( paths.processed + '/apps/**/css/*' );
  cb();
} );

// Clean JavaScript out of /cfgov/static_built/js/
gulp.task( 'clean:js', cb => {
  del( paths.processed + '/js/**/*' );
  del( paths.processed + '/apps/**/js/*' );
  cb();
} );

// Clean everything out of /cfgov/static_built/
gulp.task( 'clean', () => del( paths.processed + '/**/*' ) );
