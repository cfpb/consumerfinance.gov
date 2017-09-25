'use strict';

const chai = require( 'chai' );
const expect = chai.expect;
const fs = require( 'fs' );
const SCRIPTS_DIR = 'cfgov/static_built/js/';
const scritpsManifest = require( '../../../../gulp/utils/scripts-manifest' );
const directoryMap = scritpsManifest.getDirectoryMap( 'cfgov/static_built/js/' );
const { defineSupportCode } = require( 'cucumber' );


defineSupportCode( function( { When, Given } ) {

  Given( /I run gulp build/,

    function( ) {

      return expect( 'routes/common.js' in directoryMap )
             .to.equal( true );
    }
  );

  When( /the js bundles shouldn't contain double arrows or constants/,
    function( ) {
      const transpileRegex = /\(\)\s?=>|const .*=/g;
      const directoryMapKeys = Object.keys( directoryMap );
      const directoryMapLength = directoryMapKeys.length;

      return new Promise( function( resolve, reject ) {
        for ( let i = 0; i < directoryMapLength; i++ ) {
          fs.readFile( SCRIPTS_DIR + directoryMapKeys[i], 'utf8', function( error, contents ) {
            if ( error ) {
              reject( error );
            } else {
              const isFailure = transpileRegex.test( contents );
              if ( isFailure ) {
                reject( directoryMapKeys[i] + ' contains const or ()=>' );
              } else if ( i === directoryMapLength - 1 ) {
                resolve();
              }
            }
          } );
        }
      } );
    }
  );
} );
