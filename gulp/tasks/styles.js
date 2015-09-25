'use strict';

var gulp = require( 'gulp' );
var $ = require( 'gulp-load-plugins' )();
var mqr = require( 'gulp-mq-remove' );
var pkg = require( '../config' ).pkg;
var banner = require( '../config' ).banner;
var config = require( '../config' ).styles;
var handleErrors = require( '../utils/handleErrors' );
var browserSync = require( 'browser-sync' );

gulp.task( 'styles:modern', function() {
  return gulp.src( config.cwd + config.src )
    .pipe( $.sourcemaps.init() )
    .pipe( $.less( config.settings ) )
    .on( 'error', handleErrors )
    .pipe( $.replace(
      /url\('chosen-sprite.png'\)/ig,
      'url("/img/chosen-sprite.png")'
    ) )
    .pipe( $.replace(
      /url\('chosen-sprite@2x.png'\)/ig,
      'url("/img/chosen-sprite@2x.png")'
    ) )
    .pipe( $.autoprefixer( {
      browsers: [ 'last 2 version' ]
    } ) )
    .pipe( $.header( banner, { pkg: pkg } ) )
    .pipe( $.sourcemaps.write( '.' ) )
    .pipe( gulp.dest( config.dest ) )
    .pipe( browserSync.reload( {
      stream: true
    } ) );
} );

gulp.task( 'styles:ie', function() {
  return gulp.src( config.cwd + config.src )
    .pipe( $.less( config.settings ) )
    .on( 'error', handleErrors )
    .pipe( $.replace(
      /url\('chosen-sprite.png'\)/ig,
      'url("/img/chosen-sprite.png")'
    ) )
    .pipe( $.replace(
      /url\('chosen-sprite@2x.png'\)/ig,
      'url("/img/chosen-sprite@2x.png")'
    ) )
    .pipe( $.autoprefixer( {
      browsers: [ 'IE 7', 'IE 8' ]
    } ) )
    .pipe( mqr( {
      width: '75em'
    } ) )
    .pipe( $.cssmin() )
    .pipe( $.rename( {
      suffix:  '.ie',
      extname: '.css'
    } ) )
    .pipe( gulp.dest( config.dest ) )
    .pipe( browserSync.reload( {
      stream: true
    } ) );
} );

gulp.task( 'styles', [
  'styles:modern',
  'styles:ie'
] );
