'use strict';

var gulp = require( 'gulp' );
var gulpChanged = require( 'gulp-changed' );
var gulpReplace = require( 'gulp-replace' );
var configCopy = require( '../config' ).copy;
var handleErrors = require( '../utils/handle-errors' );
var browserSync = require( 'browser-sync' );

/**
 * Generic copy files flow from source to destination.
 * @param {string} src The path to the source files.
 * @param {string} dest The path to destination.
 * @returns {Object} An output stream from gulp.
 */
function _genericCopy( src, dest ) {
  return gulp.src( src )
    .pipe( gulpChanged( dest ) )
    .on( 'error', handleErrors )
    .pipe( gulp.dest( dest ) )
    .pipe( browserSync.reload( {
      stream: true
    } ) );
}

gulp.task( 'copy:icons', function() {
  var icons = configCopy.icons;
  return _genericCopy( icons.src, icons.dest );
} );

gulp.task( 'copy:codeJson', function() {
  var codeJson = configCopy.codejson;
  return _genericCopy( codeJson.src, codeJson.dest );
} );

gulp.task( 'copy:vendorfonts', function() {
  var vendorFonts = configCopy.vendorFonts;
  return _genericCopy( vendorFonts.src, vendorFonts.dest );
} );

gulp.task( 'copy:vendorcss', function() {
  var vendorCss = configCopy.vendorCss;
  return gulp.src( vendorCss.src )
    .pipe( gulpChanged( vendorCss.dest ) )
    .on( 'error', handleErrors )
    .pipe( gulpReplace(
      /url\(".\/ajax-loader.gif"\)/ig,
      'url("/img/ajax-loader.gif")'
    ) )
    .pipe( gulp.dest( vendorCss.dest ) )
    .pipe( browserSync.reload( {
      stream: true
    } ) );
} );

gulp.task( 'copy:vendorimg', function() {
  var vendorImg = configCopy.vendorImg;
  return _genericCopy( vendorImg.src, vendorImg.dest );
} );

gulp.task( 'copy:vendorjs', function() {
  var vendorJs = configCopy.vendorJs;
  return _genericCopy( vendorJs.src, vendorJs.dest );
} );

gulp.task( 'copy',
  [
    'copy:icons',
    'copy:codeJson',
    'copy:vendorfonts',
    'copy:vendorcss',
    'copy:vendorimg',
    'copy:vendorjs'
  ]
);
