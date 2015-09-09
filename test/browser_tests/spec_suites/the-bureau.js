'use strict';

var TheBureauPage = require( '../page_objects/page_the-bureau.js' );

describe( 'The Bureau Page', function() {
  var page;

  beforeAll( function() {
    page = new TheBureauPage();
    page.get();
  } );

  it( 'should properly load in a browser',
    function() {
      expect( page.pageTitle() ).toBe( 'The Bureau' );
    }
  );
} );
