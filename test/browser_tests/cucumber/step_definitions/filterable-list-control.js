'use strict';


var filterableListControl = require( '../../shared_objects/filterable-list-control.js' );
var { defineSupportCode } = require( 'cucumber' );
var { expect } = require( 'chai' );

defineSupportCode( function( { Then, When } ) {
  When( /I (.*) the filterable list control/, function( action ) {

    return filterableListControl[action]();
  } );
} );
