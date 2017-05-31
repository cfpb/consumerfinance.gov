'use strict';

var notify = require( 'gulp-notify' );

module.exports = function( err, exitProcess = false ) {
  var args = Array.prototype.slice.call( arguments );

  // Send error to notification center with gulp-notify
  notify.onError( {
    title:   'Compile Error',
    message: '<%= error %>'
  } ).apply( this, args );

  // Keep gulp from hanging on this task
  this.emit( 'end' );

  console.log( exitProcess.error, 'err' )
  if ( exitProcess === true ) {
    process.exit( 1 );
  }
};
