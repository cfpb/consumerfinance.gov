'use strict';

var browserSync = require( 'browser-sync' );
var config = require( '../config' );
var configPkg = config.pkg;
var configBanner = config.banner;
var configStyles = config.styles;
var configLegacy = config.legacy;
var gulp = require( 'gulp' );
var gulpAutoprefixer = require( 'gulp-autoprefixer' );
var gulpCleanCss = require( 'gulp-clean-css' );
var gulpHeader = require( 'gulp-header' );
var gulpLess = require( 'gulp-less' );
var gulpRename = require( 'gulp-rename' );
var gulpSourcemaps = require( 'gulp-sourcemaps' );
var handleErrors = require( '../utils/handle-errors' );
var mqr = require( 'gulp-mq-remove' );

/**
 * Process modern CSS.
 * @returns {PassThrough} A source stream.
 */
function stylesModern() {
  return gulp.src( configStyles.cwd + configStyles.src )
    .pipe( gulpSourcemaps.init() )
    .pipe( gulpLess( configStyles.settings ) )
    .on( 'error', handleErrors.bind( this, { exitProcess: true } ) )
    .pipe( gulpAutoprefixer( { browsers: [
      'last 2 version',
      'not ie <= 8',
      'android 4',
      'BlackBerry 7',
      'BlackBerry 10'
    ]} ) )
    .pipe( gulpHeader( configBanner, { pkg: configPkg } ) )
    .pipe( gulpSourcemaps.write( '.' ) )
    .pipe( gulp.dest( configStyles.dest ) )
    .pipe( browserSync.reload( {
      stream: true
    } ) );
}

/**
 * Process legacy CSS for IE9 only.
 * @returns {PassThrough} A source stream.
 */
function stylesIE9() {
  return gulp.src( configStyles.cwd + configStyles.src )
    .pipe( gulpLess( configStyles.settings ) )
    .on( 'error', handleErrors )
    .pipe( gulpAutoprefixer( {
      browsers: [ 'ie 9' ]
    } ) )
    .pipe( gulpRename( {
      suffix:  '.ie9',
      extname: '.css'
    } ) )
    .pipe( gulpCleanCss( {
      compatibility: 'ie9',
      inline: ['none']
    } ) )
    .pipe( gulp.dest( configStyles.dest ) )
    .pipe( browserSync.reload( {
      stream: true
    } ) );
}

/**
 * Process legacy CSS for IE7 and 8 only.
 * @returns {PassThrough} A source stream.
 */
function stylesIE8() {
  return gulp.src( configStyles.cwd + configStyles.src )
    .pipe( gulpLess( configStyles.settings ) )
    .on( 'error', handleErrors )
    .pipe( gulpAutoprefixer( {
      browsers: [ 'ie 7-8' ]
    } ) )
    .pipe( mqr( {
      width: '75em'
    } ) )
    // mqr expands the minified file
    .pipe( gulpCleanCss( { compatibility: 'ie8' } ) )
    .pipe( gulpRename( {
      suffix:  '.ie8',
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
    .pipe( gulpLess( configStyles.settings ) )
    .on( 'error', handleErrors )
    .pipe( gulpAutoprefixer( { browsers: [
      'last 2 version',
      'ie 7-8',
      'android 4',
      'BlackBerry 7',
      'BlackBerry 10'
    ]} ) )
    .pipe( gulpHeader( configBanner, { pkg: configPkg } ) )
    .pipe( gulp.dest( configStyles.dest ) )
    .pipe( mqr( {
      width: '75em'
    } ) )
    // mqr expands the minified file
    .pipe( gulpCleanCss( { compatibility: 'ie8' } ) )
    .pipe( gulpRename( {
      suffix:  '.nonresponsive',
      extname: '.css'
    } ) )
    .pipe( gulp.dest( configStyles.dest ) )
    .pipe( browserSync.reload( {
      stream: true
    } ) );
}

/**
 * Process CSS for Wagtail feature flags.
 * @returns {PassThrough} A source stream.
 */
function stylesFeatureFlags() {
  return gulp.src( configStyles.cwd + '/feature-flags/*.less' )
    .pipe( gulpLess( configStyles.settings ) )
    .on( 'error', handleErrors )
    .pipe( gulpAutoprefixer( { browsers: [
      'last 2 version',
      'ie 7-8',
      'android 4',
      'BlackBerry 7',
      'BlackBerry 10'
    ]} ) )
    .pipe( gulp.dest( configStyles.dest + '/feature-flags' ) )
    .pipe( browserSync.reload( {
      stream: true
    } ) );
}


/**
 * Process AskCFPB CSS.
 * @returns {PassThrough} A source stream.
 */
function stylesKnowledgebaseProd() {
  return gulp.src( configLegacy.cwd +
    '/knowledgebase/less/es-ask-styles.less' )
    .pipe( gulpLess( { compress: true } ) )
    .on( 'error', handleErrors )
    .pipe( gulpAutoprefixer( { browsers: [
      'last 2 version',
      'not ie <= 8',
      'android 4',
      'BlackBerry 7',
      'BlackBerry 10'
    ]} ) )
    .pipe( gulpHeader( configBanner, { pkg: configPkg } ) )
    .pipe( gulpRename( 'es-ask-styles.min.css' ) )
    .pipe( gulp.dest( configLegacy.dest + '/knowledgebase/' ) )
    .pipe( browserSync.reload( {
      stream: true
    } ) );
}

/**
 * Process AskCFPB IE CSS.
 * @returns {PassThrough} A source stream.
 */
function stylesKnowledgebaseIE() {
  return gulp.src( configLegacy.cwd +
    '/knowledgebase/less/es-ask-styles-ie.less' )
    .pipe( gulpLess( { compress: true } ) )
    .on( 'error', handleErrors )
    .pipe( gulpAutoprefixer( { browsers: [
      'last 2 version',
      'not ie <= 8',
      'android 4',
      'BlackBerry 7',
      'BlackBerry 10'
    ]} ) )
    .pipe( gulpHeader( configBanner, { pkg: configPkg } ) )
    .pipe( gulpRename( 'es-ask-styles-ie.min.css' ) )
    .pipe( gulp.dest( configLegacy.dest + '/knowledgebase/' ) )
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
    .pipe( gulpLess( { compress: true } ) )
    .on( 'error', handleErrors )
    .pipe( gulpAutoprefixer( { browsers: [
      'last 2 version',
      'not ie <= 8',
      'android 4',
      'BlackBerry 7',
      'BlackBerry 10'
    ]} ) )
    .pipe( gulpHeader( configBanner, { pkg: configPkg } ) )
    .pipe( gulpRename( 'es-styles.min.css' ) )
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
    .pipe( gulpLess( { compress: true } ) )
    .on( 'error', handleErrors )
    .pipe( gulpAutoprefixer( { browsers: [
      'last 2 version',
      'not ie <= 8',
      'android 4',
      'BlackBerry 7',
      'BlackBerry 10'
    ]} ) )
    .pipe( gulpHeader( configBanner, { pkg: configPkg } ) )
    .pipe( gulpRename( 'es-styles-ie.min.css' ) )
    .pipe( gulp.dest( configLegacy.dest + '/nemo/_/c/' ) )
    .pipe( browserSync.reload( {
      stream: true
    } ) );
}

gulp.task( 'styles:modern', stylesModern );
gulp.task( 'styles:stylesIE8', stylesIE8 );
gulp.task( 'styles:stylesIE9', stylesIE9 );
gulp.task( 'styles:ondemand', stylesOnDemand );
gulp.task( 'styles:featureFlags', stylesFeatureFlags );
gulp.task( 'styles:knowledgebase', stylesKnowledgebaseProd );
gulp.task( 'styles:knowledgebaseIE', stylesKnowledgebaseIE );
gulp.task( 'styles:nemoProd', stylesNemoProd );
gulp.task( 'styles:nemoIE', stylesNemoIE );
gulp.task( 'styles:nemo', [
  'styles:nemoProd',
  'styles:nemoIE'
] );
gulp.task( 'styles:ie', ['styles:stylesIE8', 'styles:stylesIE9'] );

gulp.task( 'styles', [
  'styles:modern',
  'styles:ie',
  'styles:ondemand',
  'styles:featureFlags',
  'styles:knowledgebase',
  'styles:knowledgebaseIE',
  'styles:nemo'
] );
