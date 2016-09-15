'use strict';

var Blog = require( '../../page_objects/page_blog.js' );

describe( 'Browse filterable', function() {

  describe( 'pagination', function() {
    var page;

    beforeEach( function() {
      page = new Blog();
      page.get();
    } );

    it( 'should navigate to the first page of filtered results', function() {
      page.searchFilterBtn.click();
      browser.wait( page.searchCategoryLabel.isEnabled() ).then( function() {
        page.searchCategoryLabel.click();
        browser.wait( page.searchFilterSubmitBtn.isEnabled() ).then( function() {
          page.searchFilterSubmitBtn.click().then( function() {
            expect( browser.getCurrentUrl() ).not.toContain( 'page=' );
            expect( browser.getCurrentUrl() ).toContain( 'at-the-cfpb' );
          } );
        } );
      } );
    } );

    it( 'should navigate to the second filtered page', function() {
      page.searchFilterBtn.click();
      browser.wait( page.searchCategoryLabel.isEnabled() ).then( function() {
        page.searchCategoryLabel.click();
        browser.wait( page.searchFilterSubmitBtn.isEnabled() ).then( function() {
          page.searchFilterSubmitBtn.click();
          browser.wait( page.paginationNextBtn.isEnabled() ).then( function() {

            // Save current URL, perform action, then wait for URL to change.
            var currentUrl;
            browser.getCurrentUrl().then( function( url ) {
              currentUrl = url;
              // Do action that changes the URL.
              page.paginationNextBtn.click();
            } ).then( function() {
              browser.wait( function() {
                // The URL has changed.
                return browser.getCurrentUrl().then( function( url ) {
                  return url !== currentUrl;
                } );
              } );
            } ).then( function() {
              // Perform tests on changed URL.
              expect( browser.getCurrentUrl() ).toContain( 'page=2' );
              expect( browser.getCurrentUrl() ).toContain( 'at-the-cfpb' );
            } );
          } );
        } );
      } );
    } );

    it( 'should navigate to the fifth filtered page', function() {
      page.searchFilterBtn.click();
      browser.wait( page.searchCategoryLabel.isEnabled() ).then( function() {
        page.searchCategoryLabel.click();
        browser.wait( page.searchFilterSubmitBtn.isEnabled() ).then( function() {
          page.searchFilterSubmitBtn.click();
          browser.wait( page.paginationPageBtn.isDisplayed() ).then( function() {

            // Save current URL, perform action, then wait for URL to change.
            var currentUrl;
            browser.getCurrentUrl().then( function( url ) {
              currentUrl = url;
              // Do action that changes the URL.
              page.paginationPageInput.clear().sendKeys( '5' );
              page.paginationPageBtn.click();
            } ).then( function() {
              browser.wait( function() {
                // The URL has changed.
                return browser.getCurrentUrl().then( function( url ) {
                  return url !== currentUrl;
                } );
              } );
            } ).then( function() {
              // Perform tests on changed URL.
              expect( browser.getCurrentUrl() ).toContain( 'page=5' );
              expect( browser.getCurrentUrl() ).toContain( 'at-the-cfpb' );
            } );
          } );
        } );
      } );
    } );
  } );
} );
