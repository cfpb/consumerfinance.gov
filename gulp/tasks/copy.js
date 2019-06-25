const gulp = require( 'gulp' );
const gulpChanged = require( 'gulp-changed' );
const configCopy = require( '../config' ).copy;
const handleErrors = require( '../utils/handle-errors' );

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

gulp.task( 'copy:icons:main', () => {
  const icons = configCopy.icons;
  return _genericCopy( icons.src, icons.dest );
} );

gulp.task( 'copy:icons:oah', () => {
  const icons = configCopy.icons;
  const iconsOAH = configCopy.iconsOAH;
  return _genericCopy( icons.src, iconsOAH.dest );
} );

gulp.task( 'copy:icons:r3k', () => {
  const icons = configCopy.icons;
  const iconsR3K = configCopy.iconsR3K;
  return _genericCopy( icons.src, iconsR3K.dest );
} );

// TODO: Remove when icon font is entirely deprecated.
gulp.task( 'copy:icons:old', () => {
  const icons = configCopy.iconsOld;
  return _genericCopy( icons.src, icons.dest );
} );

gulp.task( 'copy:json:code', () => {
  const jsonCode = configCopy.jsonCode;
  return _genericCopy( jsonCode.src, jsonCode.dest );
} );

gulp.task( 'copy:lightbox2', () => {
  const lightbox2 = configCopy.lightbox2;
  return _genericCopy( lightbox2.src, lightbox2.dest );
} );


gulp.task( 'copy:icons',
  gulp.parallel(
    'copy:icons:main',
    'copy:icons:oah',
    'copy:icons:r3k'
  )
);

gulp.task( 'copy',
  gulp.parallel(
    'copy:icons',
    // TODO: Remove when icon font is entirely deprecated.
    'copy:icons:old',
    'copy:json:code',
    'copy:lightbox2'
  )
);
