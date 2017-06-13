'use strict';


var multiSelect = require( '../../shared_objects/multi-select.js' );
var { defineSupportCode } = require( 'cucumber' );


defineSupportCode( function( { When } ) {
  When( 'interacting with search input', function( ) {

    return multiSelect.multiSelectSearch.click();
  } );
} );
