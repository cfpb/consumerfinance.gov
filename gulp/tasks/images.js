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
 * Move and process images for apps.
 * @returns {PassThrough} A source stream.
 */
function imagesApps() {
  const imageAppsDest = paths.processed + '/apps';
  return gulp.src( paths.unprocessed + '/apps/**/img/**' )
    .pipe( gulpChanged( imageAppsDest ) )
    .pipe( gulpImagemin( [
      imageminGifsicle(),
      imageminJpegtran(),
      imageminOptipng(),
      imageminSvgo()
    ] ) )
    .on( 'error', handleErrors )
    .pipe( gulp.dest( imageAppsDest ) );
}

/**
 * Move and process main images for the project.
 * @returns {PassThrough} A source stream.
 */
function imagesGeneral() {
  const imageDest = paths.processed + '/img';
  return gulp.src( paths.unprocessed + '/img/**' )
    .pipe( gulpChanged( imageDest ) )
    .pipe( gulpImagemin( [
      imageminGifsicle(),
      imageminJpegtran(),
      imageminOptipng(),
      imageminSvgo()
    ] ) )
    .on( 'error', handleErrors )
    .pipe( gulp.dest( imageDest ) );
}

gulp.task( 'images:apps', imagesApps );
gulp.task( 'images:general', imagesGeneral );
gulp.task( 'images', [ 'images:apps', 'images:general' ] );
