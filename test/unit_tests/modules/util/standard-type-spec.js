'use strict';

var BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';

var chai = require( 'chai' );
var expect = chai.expect;
var standardType = require( BASE_JS_PATH + 'modules/util/standard-type' );

describe( 'standard-type', function() {
  it( 'should include a standard JS data hook', function() {
    expect( standardType.JS_HOOK ).to.equal( 'data-js-hook' );
  } );

  it( 'should include a non operational function', function() {
    expect( standardType.noopFunct() ).to.be.undefined;
  } );

  it( 'should include a standard undefined reference', function() {
    expect( standardType.UNDEFINED ).to.be.undefined;
  } );
} );
