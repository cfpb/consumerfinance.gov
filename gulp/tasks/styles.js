'use strict';

var gulp = require( 'gulp' );
var plugins = require( 'gulp-load-plugins' )();
var mqr = require( 'gulp-mq-remove' );
var config = require( '../config' );
var configPkg = config.pkg;
var configBanner = config.banner;
var configStyles = config.styles;
var configLegacy = config.legacy;
var handleErrors = require( '../utils/handle-errors' );
var browserSync = require( 'browser-sync' );

/**
 * Process modern CSS.
 * @returns {PassThrough} A source stream.
 */
function stylesModern() {
  return gulp.src( configStyles.cwd + configStyles.src )
    .pipe( plugins.sourcemaps.init() )
    .pipe( plugins.less( configStyles.settings ) )
    .on( 'error', handleErrors )
    .pipe( plugins.autoprefixer( {
      browsers: [ 'last 2 version',
                  'not ie <= 8',
                  'android 4',
                  'BlackBerry 7',
                  'BlackBerry 10' ]
    } ) )
    .pipe( plugins.header( configBanner, { pkg: configPkg } ) )
    .pipe( plugins.sourcemaps.write( '.' ) )
    .pipe( gulp.dest( configStyles.dest ) )
    .pipe( browserSync.reload( {
      stream: true
    } ) );
}

/**
 * Process legacy CSS for IE7 and 8 only.
 * @returns {PassThrough} A source stream.
 */
function stylesIe() {
  return gulp.src( configStyles.cwd + configStyles.src )
    .pipe( plugins.less( configStyles.settings ) )
    .on( 'error', handleErrors )
    .pipe( plugins.autoprefixer( {
      browsers: [ 'ie 7-8' ]
    } ) )
    .pipe( mqr( {
      width: '75em'
    } ) )
    // mqr expands the minified file
    .pipe( plugins.cssmin() )
    .pipe( plugins.rename( {
      suffix:  '.ie',
      extname: '.css'
    } ) )
    .pipe( gulp.dest( configStyles.dest ) )
    .pipe( browserSync.reload( {
      stream: true
    } ) );
}

/**
 * Process stand-alone atomic component CSS.
 * @returns {PassThrough} A source stream.
 */
function stylesOnDemand() {
  return gulp.src( configStyles.cwd + '/on-demand/*.less' )
    .pipe( plugins.less( configStyles.settings ) )
    .on( 'error', handleErrors )
    .pipe( plugins.autoprefixer( {
      browsers: [ 'last 2 version',
                  'ie 7-8',
                  'android 4',
                  'BlackBerry 7',
                  'BlackBerry 10' ]
    } ) )
    .pipe( plugins.header( configBanner, { pkg: configPkg } ) )
    .pipe( gulp.dest( configStyles.dest ) )
    .pipe( mqr( {
      width: '75em'
    } ) )
    // mqr expands the minified file
    .pipe( plugins.cssmin() )
    .pipe( plugins.rename( {
      suffix:  '.nonresponsive',
      extname: '.css'
    } ) )
    .pipe( gulp.dest( configStyles.dest ) )
    .pipe( browserSync.reload( {
      stream: true
    } ) );
}

/**
 * Process Nemo CSS.
 * @returns {PassThrough} A source stream.
 */
function stylesNemoProd() {
  return gulp.src( configLegacy.cwd + '/nemo/_/c/less/es-styles.less' )
    .pipe( plugins.less( { compress: true } ) )
    .on( 'error', handleErrors )
    .pipe( plugins.autoprefixer( {
      browsers: [ 'last 2 version',
                  'not ie <= 8',
                  'android 4',
                  'BlackBerry 7',
                  'BlackBerry 10' ]
    } ) )
    .pipe( plugins.header( configBanner, { pkg: configPkg } ) )
    .pipe( plugins.rename( 'es-styles.min.css' ) )
    .pipe( gulp.dest( configLegacy.dest + '/nemo/_/c/' ) )
    .pipe( browserSync.reload( {
      stream: true
    } ) );
}

/**
 * Process Nemo IE CSS.
 * @returns {PassThrough} A source stream.
 */
function stylesNemoIE() {
  return gulp.src( configLegacy.cwd + '/nemo/_/c/less/es-styles-ie.less' )
    .pipe( plugins.less( { compress: true } ) )
    .on( 'error', handleErrors )
    .pipe( plugins.autoprefixer( {
      browsers: [ 'last 2 version',
                  'not ie <= 8',
                  'android 4',
                  'BlackBerry 7',
                  'BlackBerry 10' ]
    } ) )
    .pipe( plugins.header( configBanner, { pkg: configPkg } ) )
    .pipe( plugins.rename( 'es-styles-ie.min.css' ) )
    .pipe( gulp.dest( configLegacy.dest + '/nemo/_/c/' ) )
    .pipe( browserSync.reload( {
      stream: true
    } ) );
}

gulp.task( 'styles:modern', stylesModern );
gulp.task( 'styles:ie', stylesIe );
gulp.task( 'styles:ondemand', stylesOnDemand );
gulp.task( 'styles:nemoProd', stylesNemoProd );
gulp.task( 'styles:nemoIE', stylesNemoIE );
gulp.task( 'styles:nemo', [
  'styles:nemoProd',
  'styles:nemoIE'
] );

gulp.task( 'styles', [
  'styles:modern',
  'styles:ie',
  'styles:ondemand',
  'styles:nemo'
] );
