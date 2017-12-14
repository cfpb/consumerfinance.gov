const gulpNotify = require( 'gulp-notify' );

module.exports = function() {
  const args = Array.prototype.slice.call( arguments );
  let exitProcessParam = false;
  let errorParam = args[0] || {};
  const isWatching = this.tasks &&
                   this.tasks.browsersync &&
                   this.tasks.browsersync.done === false;

  if ( errorParam.exitProcess ) {
    exitProcessParam = errorParam.exitProcess;
    errorParam = args[1];
  }

  // Send error to notification center with gulp-notify.
  gulpNotify.onError( {
    title:   'Compile Error',
    message: '<%= error %>'
  } ).call( this, errorParam );

  if ( exitProcessParam === true && isWatching === false ) {
    process.exit( 1 );
  } else {

    // Keep gulp from hanging on this task.
    this.emit( 'end' );
  }

};
