const configClean = require( '../config' ).clean;
const del = require( 'del' );
const gulp = require( 'gulp' );

// Clean CSS out of /cfgov/static_built/css/
gulp.task( 'clean:css', () => del( configClean.css + '/**/*' ) );

// Clean JavaScript out of /cfgov/static_built/js/
gulp.task( 'clean:js', () => del( configClean.js + '/**/*' ) );

// Clean everything out of /cfgov/static_built/
gulp.task( 'clean', () => del( configClean.dest + '/**/*' ) );
