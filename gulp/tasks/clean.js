'use strict';

const configClean = require( '../config' ).clean;
const del = require( 'del' );
const gulp = require( 'gulp' );


gulp.task( 'clean:css', () => {
  // Clean CSS out of /cfgov/static_built/css/
  del( configClean.css + '/**/*' );
} );

gulp.task( 'clean:js', () => {
  // Clean JavaScript out of /cfgov/static_built/js/
  del( configClean.js + '/**/*' );
} );

gulp.task( 'clean', () => {
  // Clean everything out of /cfgov/static_built/
  del( configClean.dest + '/**/*' );
} );
