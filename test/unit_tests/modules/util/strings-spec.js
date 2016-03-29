'use strict';
var chai = require( 'chai' );
var expect = chai.expect;
var BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';
var strings = require( BASE_JS_PATH + 'modules/util/strings' );
var string;
var control;

describe( 'Strings stringEscape()', function() {

  it( 'should escape a url', function() {
    string = 'http://google.com';

    expect( strings.stringEscape( string ) )
      .to.equal( 'http://google\\.com' );
  } );

  it( 'should escape a hyphenated name', function() {
    string = 'Miller-Webster';

    expect( strings.stringEscape( string ) )
      .to.equal( 'Miller\\-Webster' );
  } );

  it( 'should escape a comma', function() {
    string = 'Students, Parents, and Teachers';

    expect( strings.stringEscape( string ) )
      .to.equal( 'Students\, Parents\, and Teachers' );
  } );
} );

describe( 'Strings stringMatch()', function() {
  it( 'should return true when testing matching strings', function() {
    string = 'Test String';
    control = 'Test String';

    expect( strings.stringMatch( control, string ) )
      .to.be.true;
  } );

  it( 'should return true when testing matching strings with differing casing',
    function() {
      string = 'test string';
      control = 'Test String';

      expect( strings.stringMatch( control, string ) )
        .to.be.true;
    }
  );

  it( 'should return false when testing differing strings', function() {
    string = 'Test String';
    control = 'Result String';

    expect( strings.stringMatch( control, string ) )
      .to.be.false;
  } );
} );
