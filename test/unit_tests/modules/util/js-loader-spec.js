'use strict';

var BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';
var chai = require( 'chai' );
var expect = chai.expect;
var jsdom = require( 'mocha-jsdom' );
var jsLoader = require( BASE_JS_PATH + 'modules/util/js-loader' );

describe( 'loadScript method', function() {
  jsdom( {
    features: {
      FetchExternalResources:   [ 'script' ],
      ProcessExternalResources: [ 'script' ],
      MutationEvents:           '2.0'
    }
  } );

  it( 'should invoke the callback method when the script loads',
    function() {
      var loaderPromise = new Promise( function( resolve, reject ) {
        var scriptLocation = 'http://code.jquery.com/jquery-1.5.min.js';
        jsLoader.loadScript( scriptLocation, function() {
          resolve( 'Callback called' );
        } );
      } );

      return loaderPromise.then( function( result ) {
        expect( result ).to.equal( 'Callback called' );
      } );
    }
  );

  // TODO: Add Test for script.onreadystatechange
} );
