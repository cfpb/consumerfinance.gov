'use strict';

var gulp = require( 'gulp' );
var $ = require( 'gulp-load-plugins' )();
var config = require( '../config' ).copy;
var handleErrors = require( '../utils/handleErrors' );
var browserSync = require( 'browser-sync' );

gulp.task( 'copy:files', function() {
  return gulp.src( config.files.src )
    .pipe( $.changed( config.files.dest ) )
    .on( 'error', handleErrors )
    .pipe( gulp.dest( config.files.dest ) )
    .pipe( browserSync.reload( {
      stream: true
    } ) );
} );

gulp.task( 'copy:legacy', function() {
  return gulp.src( config.legacy.src )
    .pipe( $.changed( config.legacy.dest ) )
    .on( 'error', handleErrors )
    .pipe( gulp.dest( config.legacy.dest ) )
    .pipe( browserSync.reload( {
      stream: true
    } ) );
} );

gulp.task( 'copy:icons', function() {
  return gulp.src( config.icons.src )
    .pipe( $.changed( config.icons.dest ) )
    .on( 'error', handleErrors )
    .pipe( gulp.dest( config.icons.dest ) )
    .pipe( browserSync.reload( {
      stream: true
    } ) );
} );

gulp.task( 'copy:vendorfonts', function() {
  return gulp.src( config.vendorfonts.src )
    .pipe( $.changed( config.vendorfonts.dest ) )
    .on( 'error', handleErrors )
    .pipe( gulp.dest( config.vendorfonts.dest ) )
    .pipe( browserSync.reload( {
      stream: true
    } ) );
} );

gulp.task( 'copy:vendorcss', function() {
  return gulp.src( config.vendorcss.src )
    .pipe( $.changed( config.vendorcss.dest ) )
    .on( 'error', handleErrors )
    .pipe( $.replace(
      /url\(".\/ajax-loader.gif"\)/ig,
      'url("/static/img/ajax-loader.gif")'
    ) )
    .pipe( gulp.dest( config.vendorcss.dest ) )
    .pipe( browserSync.reload( {
      stream: true
    } ) );
} );

gulp.task( 'copy:vendorimg', function() {
  return gulp.src( config.vendorimg.src )
    .pipe( $.changed( config.vendorimg.dest ) )
    .on( 'error', handleErrors )
    .pipe( gulp.dest( config.vendorimg.dest ) )
    .pipe( browserSync.reload( {
      stream: true
    } ) );
} );

gulp.task( 'copy:vendorjs', function() {
  return gulp.src( config.vendorjs.src )
    .pipe( $.changed( config.vendorjs.dest ) )
    .on( 'error', handleErrors )
    .pipe( gulp.dest( config.vendorjs.dest ) )
    .pipe( browserSync.reload( {
      stream: true
    } ) );
} );

gulp.task( 'copy',
  [
    'copy:files',
    'copy:legacy',
    'copy:icons',
    'copy:vendorfonts',
    'copy:vendorcss',
    'copy:vendorimg',
    'copy:vendorjs'
  ]
);
