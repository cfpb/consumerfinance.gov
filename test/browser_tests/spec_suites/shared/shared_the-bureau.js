'use strict';

var TheBureauPage = require( '../../page_objects/page_the-bureau.js' );

describe( 'The Bureau Page', function() {
  var page;

  beforeEach( function() {
    page = new TheBureauPage();
    page.get();
  } );

  it( 'should properly load in a browser',
    function() {
      expect( page.pageTitle() ).toBe( 'The Bureau' );
    }
  );

  it( 'should include 3 bureau missions, Educate, Enforce, Empower',
    function() {
      expect( page.missions ).toEqual(
        [
          {
            index: 0,
            text:  'Educate'
          },
          {
            index: 1,
            text:  'Enforce'
          },
          {
            index: 2,
            text:  'Empower'
          }
        ]
      );
    }
  );
} );
