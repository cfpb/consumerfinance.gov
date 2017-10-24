'use strict';

const configClean = require( '../config' ).clean;
const del = require( 'del' );
const gulp = require( 'gulp' );


/**
 * Cleans out built CSS files
 */
function cleanCSS() {
  del( configClean.css + '/**/*' );
}

/**
 * Cleans out built JavaScript files
 */
function cleanJS() {
  del( configClean.js + '/**/*' );
}

gulp.task( 'clean:css', cleanCSS );
gulp.task( 'clean:js', cleanJS );

gulp.task( 'clean', () => {
  // Clean everything out of /cfgov/static_built/
  del( configClean.dest + '/**/*' );
} );
