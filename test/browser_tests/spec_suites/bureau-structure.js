'use strict';

var TheBureauStructurePage =
require( '../page_objects/page_bureau-structure.js' );

describe( 'The Bureau Structure Page', function() {
  var page;

  beforeAll( function() {
    page = new TheBureauStructurePage();
    page.get();
  } );


  it( 'should properly load in a browser',
    function() {
      expect( page.pageTitle() ).toBe( 'Bureau Structure' );
    }
  );

  it( 'should have a side nav',
    function() {
      expect( page.sideNav.isPresent() ).toBe( true );
    }
  );

  it( 'should include the Director’s image',
    function() {
      expect( page.directorImage.isPresent() ).toBe( true );
    }
  );

  it( 'should include the Director’s name',
    function() {
      expect( page.directorName.isPresent() ).toBe( true );
    }
  );

  it( 'should include the Director’s title',
    function() {
      expect( page.directorTitle.isPresent() ).toBe( true );
    }
  );

  it( 'should include two org chart branches',
    function() {
      expect( page.orgChartBranches.count() ).toEqual( 2 );
    }
  );

  it( 'should include org chart parent nodes',
    function() {
      expect( page.orgChartParentNodes.count() ).toBeGreaterThan( 0 );
    }
  );

  it( 'should show org chart child nodes and they should be hidden',
    function() {
      expect( page.orgChartChildNodes.count() ).toBeGreaterThan( 0 );

      page.orgChartChildNodes.each( function( childNode ) {
        expect( childNode.isDisplayed() ).toBe( false );
      } );
    }
  );

  it( 'should include the download button',
    function() {
      expect( page.downloadBtn.isPresent() ).toBe( true );
    }
  );

  it( 'should include the speaking info',
    function() {
      expect( page.speakingInfo.isPresent() ).toBe( true );
      expect( page.speakingInfoEmail.getText() )
      .toEqual( 'cfpb.events@cfpb.gov' );
    }
  );

} );
