'use strict';

var TheBureauHistoryPage =
require( '../page_objects/page_bureau-history.js' );

describe( 'The Bureau History Page', function() {
  var page;

  beforeAll( function() {
    page = new TheBureauHistoryPage();
    page.get();
  } );


  it( 'should properly load in a browser',
    function() {
      expect( page.pageTitle() ).toBe( 'History' );
    }
  );

  it( 'should have a side nav',
    function() {
      expect( page.sideNav.isPresent() ).toBe( true );
    }
  );

  it( 'should include an intro title',
    function() {
      expect( page.introTitle.getText() )
      .toBe( 'The history of the Consumer Financial Protection Bureau' );
    }
  );

  it( 'should include an intro summary',
    function() {
      expect( page.introSummary.isPresent() ).toBe( true );
    }
  );

  it( 'should include a share section',
    function() {
      expect( page.socialMediaShare.isPresent() ).toBe( true );
    }
  );

  it( 'should include history sections',
    function() {
      expect( page.historySections.count() ).toBeGreaterThan( 1 );
    }
  );

  it( 'should include history section expandables',
    function() {
      expect( page.historySectionExpandables.count() ).toBeGreaterThan( 1 );
      expect( page.historySectionExpandables.first().getText() )
      .toContain( 'Timeline' );
    }
  );

} );
