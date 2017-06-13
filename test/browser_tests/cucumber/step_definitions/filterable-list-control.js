'use strict';


var filterableListControl = require( '../../shared_objects/filterable-list-control.js' );
var { defineSupportCode } = require( 'cucumber' );

defineSupportCode( function( { When } ) {
  When( /I (.*) the filterable list control/, function( action ) {

    return filterableListControl[action]();
  } );
} );
