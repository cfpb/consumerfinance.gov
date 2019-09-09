const gulp = require( 'gulp' );
const gulpChanged = require( 'gulp-changed' );
const handleErrors = require( '../utils/handle-errors' );
const paths = require( '../../config/environment' ).paths;

/*
  Path to the cf-icons SVG icons folder,
  which gets copied into the static directory on production
  so SVG references in CSS get resolved.
*/
const iconSrc = `${ paths.modules }/cf-icons/src/icons/*.svg`;

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

gulp.task( 'copy:root', () => {
  const stream = _genericCopy(
    `${ paths.unprocessed }/root/**/*`,
    paths.processed
  );
  return stream;
} );

gulp.task( 'copy:icons:main', () => {
  const stream = _genericCopy(
    iconSrc,
    `${ paths.processed }/icons/`
  );
  return stream;
} );

gulp.task( 'copy:icons:oah', () => {
  const stream = _genericCopy(
    iconSrc,
    `${ paths.processed }/apps/owning-a-home/icons/`
  );
  return stream;
} );

gulp.task( 'copy:icons:r3k', () => {
  const stream = _genericCopy(
    iconSrc,
    `${ paths.processed }/apps/regulations3k/icons/`
  );
  return stream;
} );

gulp.task( 'copy:icons:prepaid', () => {
  const stream = _genericCopy(
    iconSrc,
    `${ paths.processed }/apps/prepaid_agreements/icons/`
  );
  return stream;
} );

gulp.task( 'copy:lightbox2', () => {
  const stream = _genericCopy(
    `${ paths.modules }/lightbox2/dist/**/*`,
    `${ paths.processed }/lightbox2`
  );
  return stream;
} );


gulp.task( 'copy:icons',
  gulp.parallel(
    'copy:icons:main',
    'copy:icons:oah',
    'copy:icons:r3k',
    'copy:icons:prepaid'
  )
);

gulp.task( 'copy',
  gulp.parallel(
    'copy:icons',
    'copy:lightbox2',
    'copy:root'
  )
);