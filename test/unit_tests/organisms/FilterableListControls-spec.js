'use strict';
var BASE_JS_PATH = '../../../cfgov/unprocessed/js/';

var chai = require( 'chai' );
var expect = chai.expect;
var jsdom = require( 'mocha-jsdom' );

describe( 'FilterableListControls', function() {
  jsdom();

  before( function() {
    var FilterableListControls =
     require( BASE_JS_PATH + 'organisms/FilterableListControls' );
  } );

  // TODO: Implement tests.
} );
