'use strict';

var ActivityLog = require( '../../page_objects/page_activity-log.js' );

var BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';

var breakpointsConfig = require( BASE_JS_PATH + 'config/breakpoints-config' );

describe( 'The Activity Log Page', function() {
  var page;

  beforeAll( function() {
    page = new ActivityLog();
    page.get();
  } );

  it( 'should properly load in a browser', function() {
    expect( page.pageTitle() ).toContain( 'Activity Log' );
  } );

  it( 'should include a main summary', function() {
    expect( page.mainSummary.isPresent() ).toBe( true );
  } );

  it( 'should include a search filter',
    function() {
      expect( page.searchFilter.isPresent() ).toBe( true );
    }
  );

  it( 'should include a search filter button',
    function() {
      expect( page.searchFilterBtn.getText() ).toContain( 'Activity Log' );
    }
  );

  it( 'should include a visible Show button',
    function() {
      expect( page.searchFilterShowBtn.isDisplayed() ).toBe( true );
    }
  );

  if ( browser.params.windowWidth > breakpointsConfig.bpMED.min ) {
    it( 'should say "Show" on medium/large screens',
      function() {
        expect( page.searchFilterShowBtn.getText() ).toBe( 'Show' );
      }
    );
  }

  it( 'should include a hidden Hide button',
    function() {
      expect( page.searchFilterHideBtn.isDisplayed() ).toBe( false );
    }
  );

  xit( 'should include search filter results',
    function() {
      expect( page.searchFilterResults.count() ).toBeGreaterThan( 0 );
    }
  );

  it( 'should include pagination form',
    function() {
      expect( page.paginationForm.isPresent() ).toBe( true );
    }
  );

  it( 'should include a previous buttton within the pagination element',
    function() {
      expect( page.paginationPrevBtn.getText() ).toBe( 'Newer' );
    }
  );

  it( 'should include a next buttton within the pagination element',
    function() {
      expect( page.paginationNextBtn.getText() ).toBe( 'Older' );
    }
  );

  it( 'should include a page input with value set to 1',
    function() {
      expect( page.paginationPageInput.getAttribute( 'value' ) === 1 );
    }
  );

} );
