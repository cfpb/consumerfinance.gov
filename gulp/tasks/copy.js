const gulp = require( 'gulp' );
const gulpChanged = require( 'gulp-changed' );
const gulpReplace = require( 'gulp-replace' );
const configCopy = require( '../config' ).copy;
const handleErrors = require( '../utils/handle-errors' );
const browserSync = require( 'browser-sync' );
const del = require( 'del' );

/**
 * Generic copy files flow from source to destination.
 * @param {string} src The path to the source files.
 * @param {string} dest The path to destination.
 * @returns {Object} An output stream from gulp.
 */
function _genericCopy( src, dest ) {
  return gulp.src( src )
    .pipe( gulpChanged( dest ) )
    .on( 'error', handleErrors )
    .pipe( gulp.dest( dest ) )
    .pipe( browserSync.reload( {
      stream: true
    } ) );
}

gulp.task( 'copy:icons', () => {
  const icons = configCopy.icons;
  return _genericCopy( icons.src, icons.dest );
} );

gulp.task( 'copy:codeJson', () => {
  const codeJson = configCopy.codejson;
  return _genericCopy( codeJson.src, codeJson.dest );
} );

gulp.task( 'copy:vendorfonts', () => {
  const vendorFonts = configCopy.vendorFonts;
  return _genericCopy( vendorFonts.src, vendorFonts.dest );
} );

gulp.task( 'copy:vendorcss', () => {
  const vendorCss = configCopy.vendorCss;
  return gulp.src( vendorCss.src )
    .pipe( gulpChanged( vendorCss.dest ) )
    .on( 'error', handleErrors )
    .pipe( gulpReplace(
      /url\(".\/ajax-loader.gif"\)/ig,
      'url("/img/ajax-loader.gif")'
    ) )
    .pipe( gulp.dest( vendorCss.dest ) )
    .pipe( browserSync.reload( {
      stream: true
    } ) );
} );

gulp.task( 'copy:vendorimg', () => {
  const vendorImg = configCopy.vendorImg;
  return _genericCopy( vendorImg.src, vendorImg.dest );
} );

gulp.task( 'copy:timelinejs', () => {
  const timelinejs = configCopy.timelinejs;
  return _genericCopy( timelinejs.src, timelinejs.dest )
    .on( 'end', () => {
      del( timelinejs.dest + '/css/themes' );
    } );
} );

gulp.task( 'copy:lightbox2', () => {
  const lightbox2 = configCopy.lightbox2;
  return _genericCopy( lightbox2.src, lightbox2.dest );
} );

gulp.task( 'copy:vendorjs', () => {
  const vendorJs = configCopy.vendorJs;
  return _genericCopy( vendorJs.src, vendorJs.dest );
} );

gulp.task( 'copy',
  [
    'copy:icons',
    'copy:codeJson',
    'copy:vendorfonts',
    'copy:vendorcss',
    'copy:vendorimg',
    'copy:vendorjs',
    'copy:timelinejs',
    'copy:lightbox2'
  ]
);
