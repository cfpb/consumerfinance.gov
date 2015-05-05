/* ==========================================================================
   Bureau structure.
   Scripts for `/the-bureau/`.
   ========================================================================== */

'use strict';

require( 'slick' );

var breakpointHandler = require( '../../modules/breakpoint-handler' );
var BreakpointHandler = breakpointHandler.BreakpointHandler;
var MobileOnlyExpandable = breakpointHandler.MobileOnlyExpandable;

var carouselHandler;
$( 'document' ).ready( function () {
  if ( !$( 'html' ).hasClass( 'lt-ie9' ) ) {
    carouselHandler = new BreakpointHandler( {
      breakpoint: 599,
      type:       'max',
      enter:      function() {
        $( '.bureau-mission' ).slick({
          dots: true
        } );
      },
      leave:      function() {
        $( '.bureau-mission' ).unslick();
      }
    });
    $( '.expandable__mobile-only' ).each( function( i ) {
      new MobileOnlyExpandable( $( this ), 599 );
    });
  }
});
