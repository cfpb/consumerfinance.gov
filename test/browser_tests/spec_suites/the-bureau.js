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
      expect( page.pageTitle() ).toContain( 'The Bureau' );
    }
  );

  it( 'should have a side nav',
    function() {
      expect( page.sideNav.isPresent() ).toBe( true );
    }
  );

  it( 'should include the Director’s Bio',
    function() {
      expect( page.directorsBio.isPresent() ).toBe( true );
    }
  );

  it( 'should include the Deputy Director’s Bio',
    function() {
      expect( page.deputyDirectorsBio.isPresent() ).toBe( true );
    }
  );

} );
