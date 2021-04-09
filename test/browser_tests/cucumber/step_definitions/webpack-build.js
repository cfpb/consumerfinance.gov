const chai = require( 'chai' );
const expect = chai.expect;
const fs = require( 'fs' );
const SCRIPTS_DIR = 'cfgov/static_built/js/';
const scritpsManifest = require( '../../../../gulp/utils/scripts-manifest' );
const directoryMap = scritpsManifest.getDirectoryMap( SCRIPTS_DIR );
const { When, Given } = require( '@cucumber/cucumber' );

Given( /I run gulp build to generate JS bundles/, () => {
  expect( 'routes/common.js' in directoryMap ).to.equal( true );
} );

When( /the JS bundles shouldn't contain double arrows or constants/, () => {
  const transpileRegex = /\(\)\s?=>|const \w*=/g;
  const directoryMapKeys = Object.keys( directoryMap );
  const directoryMapLength = directoryMapKeys.length;

  return new Promise( ( resolve, reject ) => {
    for ( let i = 0; i < directoryMapLength; i++ ) {
      fs.readFile( SCRIPTS_DIR + directoryMapKeys[i], 'utf8',
        ( error, contents ) => {
          if ( error ) {
            reject( error );
          }

          const isFailure = transpileRegex.test( contents );
          if ( isFailure ) {
            reject(
              new Error( directoryMapKeys[i] + ' contains const or ()=>' )
            );
          } else if ( i === directoryMapLength - 1 ) {
            // All files searched.
            resolve();
          }
        }
      );
    }

  } );
} );
