'use strict';
var chai = require( 'chai' );
var expect = chai.expect;
var jsdom = require( 'mocha-jsdom' );
var getBreakpointState =
require( '../../../../cfgov/v1/preprocessed/js/modules/util/breakpoint-state.js' ).get;
var breakpointConfig =
require( '../../../../cfgov/v1/preprocessed/js/config/breakpoints-config.js' );

var breakpointState;
var configKeys;

beforeEach( function() {
  configKeys = Object.keys( breakpointConfig );
} );

describe( 'getBreakpointState', function() {

  jsdom();

  it( 'should return an object with properties from config file', function() {
    var breakpointStatekeys =
        Object.keys( breakpointConfig ).map( function( key ) {
          return key.toLowerCase().replace( 'is', '' );
        } );

    breakpointState = getBreakpointState();

    expect( breakpointState instanceof Object ).to.be.true;
    expect( configKeys.sort().join() === breakpointStatekeys.sort().join() )
    .to.be.true;
  } );

  it(
    'should return an object with one state property set to true',
    function() {

      var trueValueCount = 0;

      breakpointState = getBreakpointState();
      for ( var stateKey in breakpointState ) { // eslint-disable-line guard-for-in, no-inline-comments, max-len
        if ( breakpointState[stateKey] === true ) trueValueCount++;
      }

      expect( trueValueCount === 1 ).to.be.true;
    } );

  it(
    'should set the correct state property when passed width',
    function() {
      var width;
      var breakpointStateKey;

      for ( var rangeKey in breakpointConfig ) { // eslint-disable-line guard-for-in, no-inline-comments, max-len
        width = breakpointConfig[rangeKey].max || breakpointConfig[rangeKey].min;
        breakpointState = getBreakpointState( width );
        breakpointStateKey =
        'is' + rangeKey.charAt( 0 ).toUpperCase() + rangeKey.slice( 1 );

        expect( breakpointState[breakpointStateKey] ).to.be.true;
      }
    } );

} );
