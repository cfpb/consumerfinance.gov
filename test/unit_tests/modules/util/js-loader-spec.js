'use strict';

const BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';
const chai = require( 'chai' );
const expect = chai.expect;
const jsdom = require( 'mocha-jsdom' );
const jsLoader = require( BASE_JS_PATH + 'modules/util/js-loader' );

describe( 'loadScript method', () => {
  jsdom( {
    features: {
      FetchExternalResources:   [ 'script' ],
      ProcessExternalResources: [ 'script' ],
      MutationEvents:           '2.0'
    }
  } );

  it( 'should invoke the callback method when the script loads', () => {
    const loaderPromise = new Promise( function( resolve, reject ) {
      const scriptLocation = 'http://code.jquery.com/jquery-1.5.min.js';
      jsLoader.loadScript( scriptLocation, function() {
        resolve( 'Callback called' );
      } );
    } );

    return loaderPromise.then( result => {
      expect( result ).to.equal( 'Callback called' );
    } );
  } );

  // TODO: Add Test for script.onreadystatechange
} );
