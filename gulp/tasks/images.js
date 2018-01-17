const configImages = require( '../config' ).images;
const gulp = require( 'gulp' );
const gulpChanged = require( 'gulp-changed' );
const gulpImagemin = require( 'gulp-imagemin' );
const handleErrors = require( '../utils/handle-errors' );
const imageminGifsicle = require( 'imagemin-gifsicle' );
const imageminJpegtran = require( 'imagemin-jpegtran' );
const imageminOptipng = require( 'imagemin-optipng' );
const imageminSvgo = require( 'imagemin-svgo' );

/**
 * Minify images.
 * @returns {Object} An output stream from gulp.
 */
function images() {
  return gulp.src( configImages.src )
    .pipe( gulpChanged( configImages.dest ) )
    .pipe( gulpImagemin( [
      imageminGifsicle(),
      imageminJpegtran(),
      imageminOptipng(),
      imageminSvgo()
    ] ) )
    .on( 'error', handleErrors )
    .pipe( gulp.dest( configImages.dest ) );
}

gulp.task( 'images', images );
