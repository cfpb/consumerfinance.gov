'use strict';

var TheLeadershipCalendarPage =
require( '../../page_objects/page_leadership-calendar.js' );

var BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';

var breakpointsConfig = require( BASE_JS_PATH + 'config/breakpoints-config' );

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

  describe( 'Search Filter', function() {

    it( 'should be included',
      function() {
        expect( page.searchFilter.isPresent() ).toBe( true );
      }
    );

    it( 'should include Filter Calendars label',
      function() {
        var searchFilterBtn = page.searchFilterBtn;
        expect( searchFilterBtn.isPresent() ).toBe( true );
        expect( searchFilterBtn.getText() ).toContain( 'Filter calendars' );
      }
    );

    it( 'should include a visible Show button', function() {
      expect( page.searchFilterShowBtn.isDisplayed() ).toBe( true );
    } );

    if ( browser.params.windowWidth > breakpointsConfig.bpMED.min ) {
      it( 'should say "Show" on medium/large screens',
        function() {
          expect( page.searchFilterShowBtn.getText() ).toBe( 'Show' );
        }
      );
    }

    it( 'should include a visible Hide button when clicked', function() {
      var expectedConditions = protractor.ExpectedConditions;
      page.searchFilterBtn.click();
      browser.driver.wait(
        expectedConditions.elementToBeClickable( page.searchFilterHideBtn )
      ).then( function() {
        expect( page.searchFilterHideBtn.isDisplayed() ).toBe( true );
      } );
    } );

    it( 'should include a search filter search filter results',
      function() {
        expect( page.searchFilterResults.count() ).toBeGreaterThan( 0 );
      }
    );
  } );

  describe( 'Download Filter', function() {

    it( 'should be included',
      function() {
        expect( page.paginationForm.isPresent() ).toBe( true );
      }
    );

    it( 'should include text to download options',
      function() {
        var downloadFilterBtn = page.downloadFilterBtn;
        expect( downloadFilterBtn.isPresent() ).toBe( true );
        expect( downloadFilterBtn.getText() ).toContain( 'Download options' );
      }
    );

    it( 'should include a visible Show button', function() {
      expect( page.downloadFilterShowBtn.isDisplayed() ).toBe( true );
    } );

    it( 'should include a visible Hide button when clicked', function() {
      var expectedConditions = protractor.ExpectedConditions;
      page.downloadFilterBtn.click();
      browser.driver.wait(
        expectedConditions.elementToBeClickable( page.downloadFilterHideBtn )
      ).then( function() {
        expect( page.downloadFilterHideBtn.isDisplayed() ).toBe( true );
      } );
    } );

  } );

  it( 'should include pagination form',
    function() {
      expect( page.paginationForm.isPresent() ).toBe( true );
    }
  );

} );
