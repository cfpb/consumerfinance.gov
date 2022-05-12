// TODO: Remove jquery.
const $ = require( 'jquery' );

const Analytics = require( './Analytics' );
const getDataLayerOptions = Analytics.getDataLayerOptions;

$( document ).ready( function() {
  $( '.next-steps_controls > button' ).on( 'click', function( evt ) {
    evt.preventDefault();
    window.print();
    Analytics.sendEvent( getDataLayerOptions( 'Step Completed', 'Print' ) );
  } );
} );
