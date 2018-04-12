const autoprefixer = require( 'autoprefixer' );
const BROWSER_LIST = require( '../../config/browser-list-config' );
const browserSync = require( 'browser-sync' );
const config = require( '../config' );
const configPkg = config.pkg;
const configBanner = config.banner;
const configStyles = config.styles;
const configLegacy = config.legacy;
const fs = require( 'fs' );
const gulp = require( 'gulp' );
const gulpBless = require( 'gulp-bless' );
const gulpCleanCss = require( 'gulp-clean-css' );
const gulpHeader = require( 'gulp-header' );
const gulpLess = require( 'gulp-less' );
const gulpNewer = require( 'gulp-newer' );
const gulpPostcss = require( 'gulp-postcss' );
const gulpRename = require( 'gulp-rename' );
const gulpSourcemaps = require( 'gulp-sourcemaps' );
const handleErrors = require( '../utils/handle-errors' );
const mergeStream = require( 'merge-stream' );
const paths = require( '../../config/environment' ).paths;
const postcssUnmq = require( 'postcss-unmq' );

/**
 * Process modern CSS.
 * @returns {PassThrough} A source stream.
 */
function stylesModern() {
  return gulp.src( configStyles.cwd + configStyles.src )
    .pipe( gulpNewer( {
      dest:  configStyles.dest + '/main.css',
      extra: configStyles.otherBuildTriggerFiles
    } ) )
    .pipe( gulpSourcemaps.init() )
    .pipe( gulpLess( configStyles.settings ) )
    .on( 'error', handleErrors.bind( this, { exitProcess: true } ) )
    .pipe( gulpPostcss( [
      autoprefixer( { browsers: BROWSER_LIST.LAST_2 } )
    ] ) )
    .pipe( gulpHeader( configBanner, { pkg: configPkg } ) )
    .pipe( gulpSourcemaps.write( '.' ) )
    .pipe( gulp.dest( configStyles.dest ) )
    .pipe( browserSync.reload( {
      stream: true
    } ) );
}

/**
 * Process legacy CSS for IE9 and below.
 * @returns {PassThrough} A source stream.
 */
function stylesIE() {
  return gulp.src( configStyles.cwd + configStyles.src )
    .pipe( gulpNewer( {
      dest:  configStyles.dest + '/main.ie.css',
      extra: configStyles.otherBuildTriggerFiles
    } ) )
    .pipe( gulpLess( configStyles.settings ) )
    .on( 'error', handleErrors )
    .pipe( gulpPostcss( [
      postcssUnmq( {
        width: '75em'
      } ),
      autoprefixer( { browsers: BROWSER_LIST.ONLY_IE_8_9 } )
    ] ) )
    .pipe( gulpRename( {
      suffix:  '.ie',
      extname: '.css'
    } ) )
    .pipe( gulpBless( { cacheBuster: false, suffix: '.part' } ) )
    .pipe( gulpCleanCss( { compatibility: 'ie8', inline: false } ) )
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
    .pipe( gulpNewer( {
      dest:  configStyles.dest,
      // ext option required because this subtask uses multiple source files
      ext:   '.nonresponsive.css',
      extra: configStyles.otherBuildTriggerFiles
    } ) )
    .pipe( gulpLess( configStyles.settings ) )
    .on( 'error', handleErrors )
    .pipe( gulpPostcss( [
      autoprefixer( { browsers: BROWSER_LIST.LAST_2_IE_8_UP } )
    ] ) )
    .pipe( gulpHeader( configBanner, { pkg: configPkg } ) )
    .pipe( gulp.dest( configStyles.dest ) )
    .pipe( gulpPostcss( [
      postcssUnmq( {
        width: '75em'
      } )
    ] ) )
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
    .pipe( gulpNewer( {
      dest:  configStyles.dest + '/feature-flags',
      // ext option required because this subtask uses multiple source files
      ext:   '.css',
      extra: configStyles.otherBuildTriggerFiles
    } ) )
    .pipe( gulpLess( configStyles.settings ) )
    .on( 'error', handleErrors )
    .pipe( gulpPostcss( [
      autoprefixer( { browsers: BROWSER_LIST.LAST_2_IE_8_UP } )
    ] ) )
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
    .pipe( gulpNewer( {
      dest:  configStyles.dest + '/knowledgebase/es-ask-styles.min.css',
      extra: configStyles.otherBuildTriggerFiles
        .concat( configStyles.otherBuildTriggerFilesKBSpanish )
    } ) )
    .pipe( gulpLess( { compress: true } ) )
    .on( 'error', handleErrors )
    .pipe( gulpPostcss( [
      autoprefixer( { browsers: BROWSER_LIST.LAST_2_IE_9_UP } )
    ] ) )
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
function stylesKnowledgebaseSpanishIE8() {
  return gulp.src( configLegacy.cwd +
    '/knowledgebase/less/es-ask-styles-ie.less' )
    .pipe( gulpNewer( {
      dest:  configLegacy.dest + '/knowledgebase/es-ask-styles-ie.min.css',
      extra: configStyles.otherBuildTriggerFiles
        .concat( configStyles.otherBuildTriggerFilesKBSpanish )
    } ) )
    .pipe( gulpLess( { compress: true } ) )
    .on( 'error', handleErrors )
    .pipe( gulpPostcss( [
      autoprefixer( { browsers: BROWSER_LIST.ONLY_IE_8 } )
    ] ) )
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
    .pipe( gulpNewer( {
      dest:  configLegacy.dest + '/nemo/_/c/es-styles.min.css',
      extra: configStyles.otherBuildTriggerFiles
        .concat( configStyles.otherBuildTriggerFilesNemo )
    } ) )
    .pipe( gulpLess( { compress: true } ) )
    .on( 'error', handleErrors )
    .pipe( gulpPostcss( [
      autoprefixer( { browsers: BROWSER_LIST.LAST_2_IE_9_UP } )
    ] ) )
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
 * Process Nemo IE8 CSS.
 * @returns {PassThrough} A source stream.
 */
function stylesNemoIE8() {
  return gulp.src( configLegacy.cwd + '/nemo/_/c/less/es-styles-ie.less' )
    .pipe( gulpNewer( {
      dest:  configLegacy.dest + '/nemo/_/c/es-styles-ie.min.css',
      extra: configStyles.otherBuildTriggerFiles
        .concat( configStyles.otherBuildTriggerFilesNemo )
    } ) )
    .pipe( gulpLess( { compress: true } ) )
    .on( 'error', handleErrors )
    .pipe( gulpPostcss( [
      autoprefixer( { browsers: BROWSER_LIST.ONLY_IE_8 } )
    ] ) )
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
 * Process application CSS in /apps/.
 * @returns {PassThrough} A source stream.
 */
function stylesApps() {

  // Aggregate application namespaces that appear in unprocessed/apps.
  // eslint-disable-next-line no-sync
  let apps = fs.readdirSync( `${ paths.unprocessed }/apps/` );

  // Filter out .DS_STORE directory.
  apps = apps.filter( dir => dir.charAt( 0 ) !== '.' );

  // Process each application's CSS and store the gulp streams.
  const streams = [];
  apps.forEach( app => {
    streams.push(
      gulp.src(
        `${ paths.unprocessed }/apps/${ app }/css/main.less`,
        { allowEmpty: true }
      )
        .pipe( gulpNewer( {
          dest:  `${ paths.processed }/apps/${ app }/css/main.css`,
          extra: configStyles.otherBuildTriggerFiles
        } ) )
        .pipe( gulpSourcemaps.init() )
        .pipe( gulpLess( configStyles.settings ) )
        .on( 'error', handleErrors )
        .pipe( gulpPostcss( [
          autoprefixer( { browsers: BROWSER_LIST.LAST_2_IE_8_UP } )
        ] ) )
        .pipe( gulpBless( { cacheBuster: false, suffix: '.part' } ) )
        .pipe( gulpCleanCss( {
          compatibility: 'ie9',
          inline: [ 'none' ]
        } ) )
        .pipe( gulpHeader( configBanner, { pkg: configPkg } ) )
        .pipe( gulp.dest( `${ paths.processed }/apps/${ app }/css` ) )
        .pipe( browserSync.reload( {
          stream: true
        } ) )
    );
  } );

  // Return all app's gulp streams as a merged stream.
  return mergeStream( ...streams );
}

gulp.task( 'styles:apps', stylesApps );
gulp.task( 'styles:featureFlags', stylesFeatureFlags );
gulp.task( 'styles:ie', stylesIE );
gulp.task( 'styles:modern', stylesModern );
gulp.task( 'styles:ondemand', stylesOnDemand );

gulp.task( 'styles:knowledgebaseSpanishProd', stylesKnowledgebaseSpanishProd );
gulp.task( 'styles:knowledgebaseSpanishIE8', stylesKnowledgebaseSpanishIE8 );
gulp.task( 'styles:knowledgebaseSpanish',
  gulp.parallel(
    'styles:knowledgebaseSpanishProd',
    'styles:knowledgebaseSpanishIE8'
  )
);

gulp.task( 'styles:nemoProd', stylesNemoProd );
gulp.task( 'styles:nemoIE8', stylesNemoIE8 );
gulp.task( 'styles:nemo',
  gulp.parallel(
    'styles:nemoProd',
    'styles:nemoIE8'
  )
);

gulp.task( 'styles',
  gulp.parallel(
    'styles:apps',
    'styles:featureFlags',
    'styles:ie',
    'styles:knowledgebaseSpanish',
    'styles:modern',
    'styles:nemo',
    'styles:ondemand'
  )
);
