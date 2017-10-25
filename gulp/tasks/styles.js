'use strict';

const browserSync = require( 'browser-sync' );
const config = require( '../config' );
const configPkg = config.pkg;
const configBanner = config.banner;
const configStyles = config.styles;
const configLegacy = config.legacy;
const environment = require( '../../config/environment' );
const gulp = require( 'gulp' );
const gulpAutoprefixer = require( 'gulp-autoprefixer' );
const gulpChanged = require( 'gulp-changed' );
const gulpCleanCss = require( 'gulp-clean-css' );
const gulpHeader = require( 'gulp-header' );
const gulpLess = require( 'gulp-less' );
const gulpRename = require( 'gulp-rename' );
const gulpSourcemaps = require( 'gulp-sourcemaps' );
const handleErrors = require( '../utils/handle-errors' );
const mqr = require( 'gulp-mq-remove' );
const gulpBless = require( 'gulp-bless' );

/**
 * Process modern CSS.
 * @returns {PassThrough} A source stream.
 */
function stylesModern() {
  return gulp.src( configStyles.cwd + configStyles.src )
    .pipe( gulpChanged( configStyles.dest, { extension: '.css' } ) )
    .pipe( gulpSourcemaps.init() )
    .pipe( gulpLess( configStyles.settings ) )
    .on( 'error', handleErrors.bind( this, { exitProcess: true } ) )
    .pipe( gulpAutoprefixer( {
      browsers: environment.getSupportedBrowserList( 'css' )
    } ) )
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
    .pipe( gulpChanged( configStyles.dest, { extension: '.ie9.css' } ) )
    .pipe( gulpLess( configStyles.settings ) )
    .on( 'error', handleErrors )
    .pipe( gulpAutoprefixer( {
      browsers: [ 'ie 9' ]
    } ) )
    .pipe( gulpRename( {
      suffix:  '.ie9',
      extname: '.css'
    } ) )
    .pipe( gulpBless( { cacheBuster: false, suffix: '.part' } ) )
    .pipe( gulpCleanCss( {
      compatibility: 'ie9',
      inline: [ 'none' ]
    } ) )
    .pipe( gulp.dest( configStyles.dest ) )
    .pipe( browserSync.reload( {
      stream: true
    } ) );
}

/**
 * Process legacy CSS for 8 only.
 * @returns {PassThrough} A source stream.
 */
function stylesIE8() {
  return gulp.src( configStyles.cwd + configStyles.src )
    .pipe( gulpChanged( configStyles.dest, { extension: '.ie8.css' } ) )
    .pipe( gulpLess( configStyles.settings ) )
    .on( 'error', handleErrors )
    .pipe( gulpAutoprefixer( {
      browsers: [ 'ie 8' ]
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
    .pipe( gulpChanged( configStyles.dest, { extension: '.nonresponsive.css' } ) )
    .pipe( gulpLess( configStyles.settings ) )
    .on( 'error', handleErrors )
    .pipe( gulpAutoprefixer( {
      browsers: environment.getSupportedBrowserList( 'css' )
    } ) )
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
    .pipe( gulpChanged(
      configStyles.dest + '/feature-flags',
      { extension: '.css' }
    ) )
    .pipe( gulpLess( configStyles.settings ) )
    .on( 'error', handleErrors )
    .pipe( gulpAutoprefixer( {
      browsers: environment.getSupportedBrowserList( 'css' )
    } ) )
    .pipe( gulp.dest( configStyles.dest + '/feature-flags' ) )
    .pipe( browserSync.reload( {
      stream: true
    } ) );
}


/**
 * Process AskCFPB CSS.
 * @returns {PassThrough} A source stream.
 */
function stylesKnowledgebaseSpanishProd() {
  return gulp.src( configLegacy.cwd +
    '/knowledgebase/less/es-ask-styles.less' )
    .pipe( gulpChanged(
      configLegacy.dest + '/knowledgebase',
      { extension: '.min.css' }
    ) )
    .pipe( gulpLess( { compress: true } ) )
    .on( 'error', handleErrors )
    .pipe( gulpAutoprefixer( {
      browsers: environment.getSupportedBrowserList( 'css' )
    } ) )
    .pipe( gulpHeader( configBanner, { pkg: configPkg } ) )
    .pipe( gulpRename( {
      suffix:  '.min',
      extname: '.css'
    } ) )
    .pipe( gulp.dest( configLegacy.dest + '/knowledgebase/' ) )
    .pipe( browserSync.reload( {
      stream: true
    } ) );
}

/**
 * Process AskCFPB IE CSS.
 * @returns {PassThrough} A source stream.
 */
function stylesKnowledgebaseSpanishIE() {
  return gulp.src( configLegacy.cwd +
    '/knowledgebase/less/es-ask-styles-ie.less' )
    .pipe( gulpChanged(
      configLegacy.dest + '/knowledgebase',
      { extension: '.min.css' }
    ) )
    .pipe( gulpLess( { compress: true } ) )
    .on( 'error', handleErrors )
    .pipe( gulpAutoprefixer( {
      browsers: environment.getSupportedBrowserList( 'css' )
    } ) )
    .pipe( gulpHeader( configBanner, { pkg: configPkg } ) )
    .pipe( gulpRename( {
      suffix:  '.min',
      extname: '.css'
    } ) )
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
    .pipe( gulpChanged(
      configLegacy.dest + '/nemo/_/c/',
      { extension: '.min.css' }
    ) )
    .pipe( gulpLess( { compress: true } ) )
    .on( 'error', handleErrors )
    .pipe( gulpAutoprefixer( {
      browsers: environment.getSupportedBrowserList( 'css' )
    } ) )
    .pipe( gulpHeader( configBanner, { pkg: configPkg } ) )
    .pipe( gulpRename( {
      suffix:  '.min',
      extname: '.css'
    } ) )
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
    .pipe( gulpChanged(
      configLegacy.dest + '/nemo/_/c/',
      { extension: '.min.css' }
    ) )
    .pipe( gulpLess( { compress: true } ) )
    .on( 'error', handleErrors )
    .pipe( gulpAutoprefixer( {
      browsers: environment.getSupportedBrowserList( 'css' )
    } ) )
    .pipe( gulpHeader( configBanner, { pkg: configPkg } ) )
    .pipe( gulpRename( {
      suffix:  '.min',
      extname: '.css'
    } ) )
    .pipe( gulp.dest( configLegacy.dest + '/nemo/_/c/' ) )
    .pipe( browserSync.reload( {
      stream: true
    } ) );
}

/**
 * Process Owning a Home CSS.
 * @returns {PassThrough} A source stream.
 */
function stylesOAH() {
  return gulp.src( configStyles.cwd + '/apps/owning-a-home/main.less' )
    .pipe( gulpChanged(
      configLegacy.dest + '/oah/',
      { extension: '.css' }
    ) )
    .pipe( gulpSourcemaps.init() )
    .pipe( gulpLess( configStyles.settings ) )
    .on( 'error', handleErrors )
    .pipe( gulpAutoprefixer( {
      browsers: environment.getSupportedBrowserList( 'css' )
    } ) )
    .pipe( gulpBless( { cacheBuster: false, suffix: '.part' } ) )
    .pipe( gulpCleanCss( {
      compatibility: 'ie9',
      inline: [ 'none' ]
    } ) )
    .pipe( gulpHeader( configBanner, { pkg: configPkg } ) )
    .pipe( gulp.dest( configLegacy.dest + '/oah/' ) )
    .pipe( browserSync.reload( {
      stream: true
    } ) );
}

gulp.task( 'styles:modern', stylesModern );
gulp.task( 'styles:stylesIE8', stylesIE8 );
gulp.task( 'styles:stylesIE9', stylesIE9 );
gulp.task( 'styles:stylesOAH', stylesOAH );
gulp.task( 'styles:ondemand', stylesOnDemand );
gulp.task( 'styles:featureFlags', stylesFeatureFlags );
gulp.task( 'styles:knowledgebaseSpanishProd', stylesKnowledgebaseSpanishProd );
gulp.task( 'styles:knowledgebaseSpanishIE', stylesKnowledgebaseSpanishIE );
gulp.task( 'styles:nemoProd', stylesNemoProd );
gulp.task( 'styles:nemoIE', stylesNemoIE );

gulp.task( 'styles:ie', [
  'styles:stylesIE8',
  'styles:stylesIE9'
] );

gulp.task( 'styles:knowledgebaseSpanish', [
  'styles:knowledgebaseSpanishProd',
  'styles:knowledgebaseSpanishIE'
] );

gulp.task( 'styles:nemo', [
  'styles:nemoProd',
  'styles:nemoIE'
] );

gulp.task( 'styles', [
  'styles:modern',
  'styles:ie',
  'styles:stylesOAH',
  'styles:ondemand',
  'styles:featureFlags',
  'styles:knowledgebaseSpanish',
  'styles:nemo'
] );
