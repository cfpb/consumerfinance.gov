const gulp = require( 'gulp' );
const handleErrors = require( '../utils/handle-errors' );
const paths = require( '../../config/environment' ).paths;

/**
 * Process and copy images from a source to destination directory.
 * @param {string} src - A source directory.
 * @param {string} dest - A destination directory.
 * @returns {PassThrough} A source stream.
 */
function _genericCopy( src, dest ) {
  return gulp.src( src )
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
