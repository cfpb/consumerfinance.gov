'use strict';

var gulp = require( 'gulp' );
var $ = require( 'gulp-load-plugins' )();
var mqr = require( 'gulp-mq-remove' );
var config = require( '../config' ).styles;
var handleErrors = require( '../utils/handleErrors' );
var browserSync = require( 'browser-sync' );

gulp.task( 'ieStyles', function() {
  return gulp.src( config.cwd + config.src )
    .pipe( $.less( config.settings ) )
    .on( 'error', handleErrors )
    .pipe( $.replace(
      /url\('chosen-sprite.png'\)/ig,
      'url("/static/img/chosen-sprite.png")'
    ) )
    .pipe( $.replace(
      /url\('chosen-sprite@2x.png'\)/ig,
      'url("/static/img/chosen-sprite@2x.png")'
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
