const gulp = require( 'gulp' );
const gulpChanged = require( 'gulp-changed' );
const configCopy = require( '../config' ).copy;
const handleErrors = require( '../utils/handle-errors' );
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
    .pipe( gulp.dest( dest ) );
}

gulp.task( 'copy:icons', () => {
  const icons = configCopy.icons;
  return _genericCopy( icons.src, icons.dest );
} );

gulp.task( 'copy:jsonCode', () => {
  const jsonCode = configCopy.jsonCode;
  return _genericCopy( jsonCode.src, jsonCode.dest );
} );

gulp.task( 'copy:jsonKBYO', () => {
  const jsonKBYO = configCopy.jsonKBYO;
  return _genericCopy( jsonKBYO.src, jsonKBYO.dest );
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


gulp.task( 'copy',
  gulp.parallel(
    'copy:icons',
    'copy:jsonCode',
    'copy:jsonKBYO',
    'copy:timelinejs',
    'copy:lightbox2'
  )
);
