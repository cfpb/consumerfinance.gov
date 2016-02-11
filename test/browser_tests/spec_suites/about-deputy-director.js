'use strict';

var TheAboutDirectorPage = require( '../page_objects/page_about-director.js' );

describe( 'The About Deputy Director Page', function() {
  var page;

  beforeAll( function() {
    page = new TheAboutDirectorPage( );
    page.get( 'deputyDirector' );
  } );

  it( 'should properly load in a browser',
    function() {
      expect( page.pageTitle() ).toBe( 'About Meredith Fuchs' );
    }
  );

  it( 'should have a side nav',
    function() {
      expect( page.sideNav.isPresent() ).toBe( true );
    }
  );

  it( 'should include the Deputy Director’s bio',
    function() {
      expect( page.directorBioSummary.isPresent() ).toBe( true );
    }
  );

  it( 'should include the Deputy Director’s summary',
    function() {
      expect( page.directorBioSummary.isPresent() ).toBe( true );
    }
  );

  it( 'should include the Deputy Director’s title',
    function() {
      expect( page.directorTitle.getText() )
      .toEqual( 'Deputy Director Meredith Fuchs (Acting)' );
    }
  );

  it( 'should include the Deputy Director’s image',
    function() {
      expect( page.directorImage.isPresent() ).toBe( true );
    }
  );

  it( 'should include a More Info section',
    function() {
      expect( page.moreInfo.isPresent() ).toBe( true );
    }
  );

  it( 'should include a More Info title',
    function() {
      expect( page.moreInfoTitle.getText() )
      .toEqual( 'More information about Meredith Fuchs' );
    }
  );

  it( 'should include three More Info items',
    function() {
      expect( page.moreInfoItems.count() ).toEqual( 3 );
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

  it( 'should include a Related Links section',
    function() {
      expect( page.relatedLinks.isPresent() ).toBe( true );
    }
  );

  it( 'should include a Share section',
    function() {
      expect( page.socialMediaShare.isPresent() ).toBe( true );
    }
  );

} );
