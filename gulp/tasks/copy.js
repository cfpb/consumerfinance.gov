'use strict';

var gulp = require( 'gulp' );
var $ = require( 'gulp-load-plugins' )();
var config = require( '../config' ).copy;
var handleErrors = require( '../utils/handleErrors' );
var browserSync = require( 'browser-sync' );

/**
 * Generic copy files flow from source to destination.
 * @param {string} src The path to the source files.
 * @param {string} dest The path to destination.
 * @returns {Object} An output stream from gulp.
 */
function _genericCopy( src, dest ) {
  return gulp.src( src )
    .pipe( $.changed( dest ) )
    .on( 'error', handleErrors )
    .pipe( gulp.dest( dest ) )
    .pipe( browserSync.reload( {
      stream: true
    } ) );
}

gulp.task( 'copy:icons', function() {
  return _genericCopy( config.icons.src, config.icons.dest );
} );

gulp.task( 'copy:vendorfonts', function() {
  return _genericCopy( config.vendorfonts.src, config.vendorfonts.dest );
} );

gulp.task( 'copy:vendorcss', function() {
  return gulp.src( config.vendorcss.src )
    .pipe( $.changed( config.vendorcss.dest ) )
    .on( 'error', handleErrors )
    .pipe( $.replace(
      /url\(".\/ajax-loader.gif"\)/ig,
      'url("/img/ajax-loader.gif")'
    ) )
    .pipe( gulp.dest( config.vendorcss.dest ) )
    .pipe( browserSync.reload( {
      stream: true
    } ) );
} );

gulp.task( 'copy:vendorimg', function() {
  return _genericCopy( config.vendorimg.src, config.vendorimg.dest );
} );

gulp.task( 'copy:vendorjs', function() {
  return _genericCopy( config.vendorjs.src, config.vendorjs.dest );
} );

gulp.task( 'copy',
  [
    'copy:icons',
    'copy:vendorfonts',
    'copy:vendorcss',
    'copy:vendorimg',
    'copy:vendorjs'
  ]
);
