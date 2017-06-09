'use strict';

const gulpNotify = require( 'gulp-notify' );

module.exports = function() {
  var args = Array.prototype.slice.call( arguments );
  var exitProcessParam = false;
  var errorParam = args[0] || {};

  if ( errorParam.hasOwnProperty( 'exitProcess' ) ) {
    exitProcessParam = errorParam.exitProcess;
    errorParam = args[1];
  }

  // Send error to notification center with gulp-notify.
  gulpNotify.onError( {
    title:   'Compile Error',
    message: '<%= error %>'
  } ).call( this, errorParam );

  // Keep gulp from hanging on this task.
  this.emit( 'end' );

  if ( exitProcessParam === true ) {
    process.exit( 1 );
  }
};
