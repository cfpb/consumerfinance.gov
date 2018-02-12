/* gulpfile.js
   ===========
   Rather than manage one giant configuration file responsible
   for creating multiple tasks, each task has been broken out into
   its own file in gulp/tasks. Any files in that directory get
   automatically required below.
   To add a new task, simply add a new task file the gulp/tasks directory.
   gulp/tasks/default.js specifies the default set of tasks to run
   when you run `gulp`. */

const gulp = require( 'gulp' );
const requireDir = require( 'require-dir' );

// Require all tasks in gulp/tasks, including subfolders.
requireDir( './gulp/tasks', { recurse: true } );

gulp.task( 'build',
  gulp.series(
    gulp.parallel(
      'styles',
      'scripts',
      'images'
    ),
    'copy'
  )
);

gulp.task( 'default',
  gulp.parallel(
    'build',
    'lint:scripts',
    'test:unit'
  )
);
