'use strict';

var TheAboutDirectorPage = require( '../page_objects/page_about-director.js' );

describe( 'The About Director Page', function() {
  var page;

  beforeAll( function() {
    page = new TheAboutDirectorPage( );
    page.get( 'director' );
  } );


  it( 'should properly load in a browser',
    function() {
      expect( page.pageTitle() ).toBe( 'About Richard Cordray' );
    }
  );

  it( 'should have a side nav',
    function() {
      expect( page.sideNav.isPresent() ).toBe( true );
    }
  );

  it( 'should include the Director’s bio',
    function() {
      expect( page.directorBioSummary.isPresent() ).toBe( true );
    }
  );

  it( 'should include the Director’s summary',
    function() {
      expect( page.directorBioSummary.isPresent() ).toBe( true );
    }
  );

  it( 'should include Director’s image',
    function() {
      expect( page.directorImage.isPresent() ).toBe( true );
    }
  );

  it( 'should include the More Info section',
    function() {
      expect( page.moreInfo.isPresent() ).toBe( true );
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

  it( 'should include the More Info section',
    function() {
      expect( page.moreInfo.isPresent() ).toBe( true );
    }
  );

  it( 'should include the More Info title',
    function() {
      expect( page.moreInfoTitle.getText() )
      .toEqual( 'More information about Richard Cordray' );
    }
  );

  it( 'should include three More Info items',
    function() {
      expect( page.moreInfoItems.count() ).toEqual( 3 );
    }
  );

  it( 'should include the Related Links section',
    function() {
      expect( page.relatedLinks.isPresent() ).toBe( true );
    }
  );

  it( 'should include the Share section',
    function() {
      expect( page.socialMediaShare.isPresent() ).toBe( true );
    }
  );

  it( 'should include the Speaking info section',
    function() {
      expect( page.speakingInfo.isPresent() ).toBe( true );
    }
  );

  it( 'should include the Speaking info link',
    function() {
      expect( page.speakingInfoEmail.isPresent() ).toBe( true );
      expect( page.speakingInfoEmail.getText() )
      .toEqual( 'externalaffairs@cfpb.gov' );
    }
  );

} );
