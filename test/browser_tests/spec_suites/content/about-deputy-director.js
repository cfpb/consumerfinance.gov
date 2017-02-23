'use strict';

var TheAboutDirectorPage = require( '../../page_objects/page_about-director.js' );

describe( 'The About Deputy Director Page', function() {
  var page;

  beforeAll( function() {
    page = new TheAboutDirectorPage( );
    page.get( 'deputyDirector' );
  } );

  it( 'should properly load in a browser',
    function() {
      expect( page.pageTitle() ).toContain( 'About David Silberman' );
    }
  );

  it( 'should have a side nav',
    function() {
      expect( page.sideNav.isPresent() ).toBe( true );
    }
  );

  it( 'should include the Deputy Director’s bio',
    function() {
      expect( page.directorBio.isPresent() ).toBe( true );
    }
  );

  it( 'should include the Deputy Director’s image',
    function() {
      expect( page.directorImage.isPresent() ).toBe( true );
    }
  );

  it( 'should include a bio download link',
    function() {
      expect( page.bioDownload.isPresent() ).toBe( true );
    }
  );

  it( 'should include the Deputy Director’s high resolution image',
    function() {
      var highResImageDownload = page.mediaDownloads.get( 0 );
      expect( highResImageDownload.isPresent() ).toBe( true );
      expect( highResImageDownload.getText() )
      .toEqual( 'High-res portrait' );
    }
  );

  it( 'should include the Deputy Director’s low resolution image',
    function() {
      var lowResImageDownload = page.mediaDownloads.get( 1 );
      expect( lowResImageDownload.isPresent() ).toBe( true );
      expect( lowResImageDownload.getText() )
      .toEqual( 'Low-res portrait' );
    }
  );

} );
