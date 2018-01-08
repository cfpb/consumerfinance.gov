const BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';
const chai = require( 'chai' );
const expect = chai.expect;
const jsLoader = require( BASE_JS_PATH + 'modules/util/js-loader' );

describe( 'loadScript method', () => {
  before( () => {
    // Settings object passed to jsdom is for loading external resources.
    this.jsdom = require( 'jsdom-global' )( '', {
      runScripts: 'dangerously',
      resources: 'usable'
    } );
  } );

  after( () => this.jsdom() );

  it( 'should invoke the callback method when the script loads', () => {
    // eslint-disable-next-line no-unused-vars
    const loaderPromise = new Promise( ( resolve, reject ) => {
      const scriptLocation = 'http://code.jquery.com/jquery-1.5.min.js';
      jsLoader.loadScript( scriptLocation, () => {
        resolve( 'Callback called' );
      } );
    } );

    return loaderPromise.then( result => {
      expect( result ).to.equal( 'Callback called' );
    } );
  } );

  // TODO: Add Test for script.onreadystatechange
} );
