const autoprefixer = require( 'autoprefixer' );
const config = require( '../config' );
const configPkg = config.pkg;
const configBanner = config.banner;
const configStyles = config.styles;
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
      autoprefixer()
    ] ) )
    .pipe( gulpHeader( configBanner, { pkg: configPkg } ) )
    .pipe( gulpSourcemaps.write( '.' ) )
    .pipe( gulp.dest( configStyles.dest ) );
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
      autoprefixer( { overrideBrowserslist: [ 'ie 8', 'ie 9' ]} )
    ] ) )
    .pipe( gulpRename( {
      suffix:  '.ie',
      extname: '.css'
    } ) )
    .pipe( gulpBless( { cacheBuster: false, suffix: '.part' } ) )
    .pipe( gulpCleanCss( { compatibility: 'ie8', inline: false } ) )
    .pipe( gulp.dest( configStyles.dest ) );
}

/**
 * Process stand-alone atomic component CSS.
 * @returns {PassThrough} A source stream.
 */
function stylesOnDemand() {
  return gulp.src( configStyles.cwd + '/on-demand/*.less' )
    .pipe( gulpNewer( {
      dest:  configStyles.dest,
      extra: configStyles.otherBuildTriggerFiles
    } ) )
    .pipe( gulpLess( configStyles.settings ) )
    .on( 'error', handleErrors )
    .pipe( gulpPostcss( [
      autoprefixer()
    ] ) )
    .pipe( gulpHeader( configBanner, { pkg: configPkg } ) )
    .pipe( gulpCleanCss( { compatibility: '*' } ) )
    .pipe( gulp.dest( configStyles.dest ) );
}

/**
 * Process CSS for Wagtail on demand blocks.
 * @returns {PassThrough} A source stream.
 */
function stylesOnDemandBlocks() {
  return gulp.src( configStyles.cwd + '/on-demand/blocks/*.less' )
    .pipe( gulpNewer( {
      dest:  configStyles.dest + '/blocks',
      // ext option required because this subtask uses multiple source files
      ext:   '.css',
      extra: configStyles.otherBuildTriggerFiles
    } ) )
    .pipe( gulpLess( configStyles.settings ) )
    .on( 'error', handleErrors )
    .pipe( gulpPostcss( [
      autoprefixer()
    ] ) )
    .pipe( gulp.dest( configStyles.dest + '/on-demand' ) );
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
      autoprefixer()
    ] ) )
    .pipe( gulp.dest( configStyles.dest + '/feature-flags' ) );
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
          autoprefixer()
        ] ) )
        .pipe( gulpBless( { cacheBuster: false, suffix: '.part' } ) )
        .pipe( gulpCleanCss( {
          compatibility: 'ie9',
          inline: [ 'none' ]
        } ) )
        .pipe( gulpHeader( configBanner, { pkg: configPkg } ) )
        .pipe( gulp.dest( `${ paths.processed }/apps/${ app }/css` ) )
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
gulp.task( 'styles:ondemandBlocks', stylesOnDemandBlocks );


gulp.task( 'styles',
  gulp.parallel(
    'styles:apps',
    'styles:featureFlags',
    'styles:ie',
    'styles:modern',
    'styles:ondemand',
    'styles:ondemandBlocks'
  )
);

gulp.task( 'styles:watch', function() {
  gulp.watch(
    `${ configStyles.cwd }/**/*.less`,
    gulp.parallel( 'styles:modern' )
  );
  gulp.watch(
    `${ paths.unprocessed }/**/css/**/*.less`,
    gulp.series( 'styles:apps' )
  );
} );
