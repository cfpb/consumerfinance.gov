const BASE_JS_PATH = '../../../../../cfgov/unprocessed/js/';
const jsLoader = require( BASE_JS_PATH + 'modules/util/js-loader' );

describe( 'loadScript method', () => {

  /* TODO: Jest doesn't currently expose runscripts: 'dangerously'
     Find a way to do this. See
     https://www.npmjs.com/package/@mediaeventservices/jest-environment-jsdom-external-scripts */

  xit( 'should invoke the callback method when the script loads', () => {
    // eslint-disable-next-line no-unused-vars
    const loaderPromise = new Promise( ( resolve, reject ) => {
      const scriptLocation = 'https://code.jquery.com/jquery-1.5.min.js';
      jsLoader.loadScript( scriptLocation, () => {
        resolve( 'Callback called' );
      } );
    } );

    return loaderPromise.then( result => {
      expect( result ).toEqual( 'Callback called' );
    } );
  } );

  // TODO: Add Test for script.onreadystatechange
} );
