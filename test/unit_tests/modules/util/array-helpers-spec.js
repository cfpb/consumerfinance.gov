'use strict';
var chai = require( 'chai' );
var expect = chai.expect;
var jsdom = require( 'mocha-jsdom' );
var BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';
var ERROR_MESSAGES = require( BASE_JS_PATH + 'config/error-messages-config' );
var arrayHelpers = require( BASE_JS_PATH + 'modules/util/array-helpers' );
var array;
var index;

describe( 'Array Helpers indexOfObject', function() {

  it( 'should return -1 if the array is empty', function() {
    array = [];
    index = arrayHelpers.indexOfObject( array, 'foo' );

    expect( index ).to.equal( -1 );
  } );

  it( 'should return -1 if there is no match', function() {
    array = [
      { 'value': 'bar' },
      { 'value': 'baz' }
    ];
    index = arrayHelpers.indexOfObject( array, 'value', 'foo' );

    expect( index ).to.equal( -1 );
  } );

  it( 'should return the matched index', function() {
    array = [
      { 'value': 'foo' },
      { 'value': 'bar' },
      { 'value': 'baz' }
    ];
    index = arrayHelpers.indexOfObject( array, 'value', 'foo' );

    expect( index ).to.equal( 0 );
  } );
} );
