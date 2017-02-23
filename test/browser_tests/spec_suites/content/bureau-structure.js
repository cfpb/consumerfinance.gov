'use strict';

var BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';

var breakpointsConfig = require( BASE_JS_PATH + 'config/breakpoints-config' );

var TheBureauStructurePage =
  require( '../../page_objects/page_bureau-structure.js' );

describe( 'The Bureau Structure Page', function() {
  var page;
  var _expectedConditions = protractor.ExpectedConditions;
  var _expandable;

  beforeAll( function() {
    page = new TheBureauStructurePage();
    page.get();
  } );

  // Check large size.
  if ( browser.params.windowWidth > breakpointsConfig.bpLG.min ) {
    describe( 'large size', function() {

      it( 'should properly load in a browser',
        function() {
          expect( page.pageTitle() ).toContain( 'Bureau Structure' );
        }
      );

      it( 'should have a secondary navigation',
        function() {
          expect( page.secondaryNavigation.isPresent() ).toBe( true );
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

          browser.getCapabilities().then( function( cap ) {
            browser.name = cap.get( 'browserName' );
            browser.version = cap.get( 'version' );
          } );
          var ie8 = browser.name === 'internet explorer' &&
                    browser.version === '8';

          if ( !ie8 ) {
            page.orgChartChildNodes.each( function( childNode ) {
              expect( childNode.isDisplayed() ).toBe( false );
            } );
          }
        }
      );

      it( 'should include the download button',
        function() {
          expect( page.downloadBtn.isPresent() ).toBe( true );
        }
      );
    } );
  } else if ( browser.params.windowWidth < breakpointsConfig.bpXS.max ) {
    describe( 'extra small size', function() {

      describe( 'on page load', function() {
        it( 'should NOT display org chart children', function() {
          expect( page.orgChartChildNodes.first().isDisplayed() ).toBe( false );
        } );
      } );

      describe( 'when clicking chart node', function() {
        beforeEach( function() {
          page.get();
          page.orgChartCategoryLinks.last().click();
          _expandable = page.getExpandableOffice();
        } );

        it( 'should display org chart children', function() {
          browser.driver.wait(
            _expectedConditions.elementToBeClickable( _expandable )
          ).then( function() {
            expect( _expandable.isDisplayed() ).toBe( true );
          } );
        } );

        it( 'should display expandable show button', function() {
          browser.driver.wait(
            _expectedConditions.elementToBeClickable( _expandable )
          ).then( function() {
            // Caveat.. if for some reason the expandable is programmatically
            // clicked when opening the org chart, this likely won't catch it
            // as the assertions will happen before the hide button shows
            // at the end of the expandable animation.
            expect( page.getExpandableHideBtn().isDisplayed() ).toBe( false );
            expect( page.getExpandableShowBtn().isDisplayed() ).toBe( true );
          } );
        } );
      } );

      describe( 'when clicking chart node expandable', function() {
        // TODO: Implement test.
        /* beforeEach( function() {
          page.get();
          page.orgChartCategoryLinks.last().click();
          _expandable = page.getExpandableOffice();
          browser.driver.wait(
            _expectedConditions.elementToBeClickable( _expandable )
          ).then( function() {
            page.getExpandableTarget().click();
          } );
        } ); */

        xit( 'should display expandable hide button', function() {
          // TODO: Implement test.
          //       Sadly, this is a difficult one, as the expandable
          //       can be clicked before it's initialized since
          //       the ContentSlider clones the expandable nodes,
          //       so it looks like it's initialized from a markup
          //       perspective before it is.
        } );
      } );

    } );
  }
} );
