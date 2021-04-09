/* eslint-disable */
// TODO: Remove jquery.
const $ = require( 'jquery' );

// To play nicer with nemo, add js class to body element
const bodyTag = document.getElementsByTagName( 'body' )[0];
bodyTag.className += ' js';

$( '.toggle-menu' ).on( 'click', function( evt ) {
  evt.preventDefault();
  $( 'nav.main ul' ).toggleClass( 'vis' );
} );
