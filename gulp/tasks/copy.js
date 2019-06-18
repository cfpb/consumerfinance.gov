const gulp = require( 'gulp' );
const gulpChanged = require( 'gulp-changed' );
const handleErrors = require( '../utils/handle-errors' );
const paths = require( '../../config/environment' ).paths;

/*
  Path to the cf-icons SVG icons folder,
  which gets copied into the static directory on production
  so SVG references in CSS get resolved.
*/
const iconSrc = paths.modules + '/cf-icons/src/icons/*.svg';

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
  return _genericCopy(
    iconSrc,
    `${ paths.processed }/icons/`
  );
} );

gulp.task( 'copy:icons:oah', () => {
  return _genericCopy(
    iconSrc,
    `${ paths.processed }/apps/owning-a-home/icons/`
  );
} );

gulp.task( 'copy:icons:r3k', () => {
  return _genericCopy(
    iconSrc,
    `${ paths.processed }/apps/regulations3k/icons/`
  );
} );

gulp.task( 'copy:json:code', () => {
  return _genericCopy(
    'code.json',
    paths.processed
  );
} );

gulp.task( 'copy:lightbox2', () => {
  return _genericCopy(
    [ `${ paths.modules }/lightbox2/dist/**/*` ],
    `${ paths.processed }/lightbox2`
  );
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
    'copy:json:code',
    'copy:lightbox2'
  )
);
