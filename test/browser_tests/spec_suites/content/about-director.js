'use strict';

var TheAboutDirectorPage = require( '../../page_objects/page_about-director.js' );

describe( 'The About Director Page', function() {
  var page;

  beforeAll( function() {
    page = new TheAboutDirectorPage( );
    page.get( 'director' );
  } );


  it( 'should properly load in a browser',
    function() {
      expect( page.pageTitle() ).toContain( 'About Richard Cordray' );
    }
  );

  it( 'should have a side nav',
    function() {
      expect( page.sideNav.isPresent() ).toBe( true );
    }
  );

  it( 'should include the Director’s bio',
    function() {
      expect( page.directorBio.isPresent() ).toBe( true );
    }
  );

  it( 'should include Director’s image',
    function() {
      expect( page.directorImage.isPresent() ).toBe( true );
    }
  );

  it( 'should include the bio download link',
    function() {
      expect( page.bioDownload.isPresent() ).toBe( true );
    }
  );

  it( 'should include the Director’s high resolution image',
    function() {
      expect( page.highResImageDownload.isPresent() ).toBe( true );
      expect( page.highResImageDownload.getText() )
      .toEqual( 'High-res portrait' );
    }
  );

  it( 'should include the Director’s low resolution image',
    function() {
      expect( page.lowResImageDownload.isPresent() ).toBe( true );
      expect( page.lowResImageDownload.getText() )
      .toEqual( 'Low-res portrait' );
    }
  );

} );
