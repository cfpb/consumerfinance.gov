'use strict';

var TheLeadershipCalendarPage =
require( '../page_objects/page_leadership-calendar.js' );

describe( 'The Leadership Calendar Page', function() {
  var page;

  beforeAll( function() {
    page = new TheLeadershipCalendarPage();
    page.get();
  } );


  it( 'should properly load in a browser',
    function() {
      expect( page.pageTitle() ).toContain( 'Leadership calendar' );
    }
  );

  it( 'should include the side nav',
    function() {
      expect( page.sideNav.isPresent() ).toBe( true );
    }
  );

  it( 'should include an intro summary',
    function() {
      expect( page.introSummary.isPresent() ).toBe( true );
    }
  );

  it( 'should include a search filter',
    function() {
      expect( page.searchFilter.isPresent() ).toBe( true );
    }
  );

  it( 'should include a search filter button',
    function() {
      var searchFilterBtn = page.searchFilterBtn;
      expect( searchFilterBtn.isPresent() ).toBe( true );
      expect( searchFilterBtn.getText() ).toContain( 'Filter calendars' );
      expect( searchFilterBtn.getText() ).toContain( 'Show' );
    }
  );

  it( 'should include a search filter search filter results',
    function() {
      expect( page.searchFilterResults.count() ).toBeGreaterThan( 0 );
    }
  );

  it( 'should include a download filter',
    function() {
      expect( page.paginationForm.isPresent() ).toBe( true );
    }
  );

  it( 'should include a download filter button',
    function() {
      var downloadFilterBtn = page.downloadFilterBtn;
      expect( downloadFilterBtn.isPresent() ).toBe( true );
      expect( downloadFilterBtn.getText() ).toContain( 'Download options' );
      expect( downloadFilterBtn.getText() ).toContain( 'Show' );
    }
  );

  it( 'should include pagination form',
    function() {
      expect( page.paginationForm.isPresent() ).toBe( true );
    }
  );

} );
