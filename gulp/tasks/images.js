const gulp = require( 'gulp' );
const gulpChanged = require( 'gulp-changed' );
const gulpImagemin = require( 'gulp-imagemin' );
const handleErrors = require( '../utils/handle-errors' );
const imageminGifsicle = require( 'imagemin-gifsicle' );
const imageminJpegtran = require( 'imagemin-jpegtran' );
const imageminOptipng = require( 'imagemin-optipng' );
const imageminSvgo = require( 'imagemin-svgo' );
const paths = require( '../../config/environment' ).paths;

/**
 * Process and copy images from a source to destination directory.
 * @param {string} src - A source directory.
 * @param {string} dest - A destination directory.
 * @returns {PassThrough} A source stream.
 */
function _genericCopy( src, dest ) {
  return gulp.src( src )
    .pipe( gulpChanged( dest ) )
    .pipe( gulpImagemin( [
      imageminGifsicle(),
      imageminJpegtran(),
      imageminOptipng(),
      imageminSvgo()
    ] ) )
    .on( 'error', handleErrors )
    .pipe( gulp.dest( dest ) );
}

/**
 * Move and process images for apps.
 * @returns {PassThrough} A source stream.
 */
function imagesApps() {
  const imageAppsSrc = paths.unprocessed + '/apps/**/img/**';
  const imageAppsDest = paths.processed + '/apps';
  return _genericCopy( imageAppsSrc, imageAppsDest );
}

/**
 * Move and process main images for the project.
 * @returns {PassThrough} A source stream.
 */
function imagesGeneral() {
  const imageGeneralSrc = paths.unprocessed + '/img/**';
  const imageGeneralDest = paths.processed + '/img';
  return _genericCopy( imageGeneralSrc, imageGeneralDest );
}

gulp.task( 'images:apps', imagesApps );
gulp.task( 'images:general', imagesGeneral );
gulp.task( 'images',
  gulp.parallel(
    'images:apps',
    'images:general'
  )
);
