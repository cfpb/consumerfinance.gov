'use strict';

var $ = require( 'jquery' );

$( "input[name='is_helpful']" ).one( 'change', function( e ) {
  // $( "input[name='is_helpful']" ).attr( 'disabled', true );
  $( '.rating-message' ).fadeIn();
  var href = $( '.feedback-link' ).attr( 'href' );
  if ( href ) {
    $( '.feedback-link' ).attr( 'href', href + '?is_helpful=' + e.target.value );
  }
} );

