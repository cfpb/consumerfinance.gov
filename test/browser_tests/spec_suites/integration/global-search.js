'use strict';

var BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';

var breakpointsConfig = require( BASE_JS_PATH + 'config/breakpoints-config' );

describe( 'GlobalSearch', function() {
  var BASE_SEL = '.m-global-search';
  var TRIGGER_SEL = BASE_SEL + ' [data-js-hook="behavior_flyout-menu_trigger"]';
  var CONTENT_SEL = BASE_SEL + ' [data-js-hook="behavior_flyout-menu_content"]';
  var INPUT_SEL = BASE_SEL + ' input#query';
  var SEARCH_SEL = BASE_SEL + ' [data-js-hook="behavior_flyout-menu_content"] .btn';
  var CLEAR_SEL = BASE_SEL + ' .input-contains-label_after';
  var SUGGEST_SEL = BASE_SEL + ' .m-global-search_content-suggestions';

  var _dom;
  var _nonLinkDom;

  beforeAll( function() {
    _nonLinkDom = element( by.css( '.o-footer_official-website' ) );
    _dom = {
      trigger:   element( by.css( TRIGGER_SEL ) ),
      content:   element( by.css( CONTENT_SEL ) ),
      input:     element( by.css( INPUT_SEL ) ),
      searchBtn: element( by.css( SEARCH_SEL ) ),
      clearBtn:  element( by.css( CLEAR_SEL ) ),
      suggest:   element( by.css( SUGGEST_SEL ) )
    };
  } );

  beforeEach( function() {
    browser.get( '/' );
  } );

  if ( browser.params.windowWidth > breakpointsConfig.bpLG.min ) {
    describe( 'large size', function() {

      describe( 'at page load', function() {
        it( 'should have a search trigger', function() {
          expect( _dom.trigger.isDisplayed() ).toBe( true );
        } );

        it( 'should NOT have search input content', function() {
          expect( _dom.content.isDisplayed() ).toBe( false );
        } );

        it( 'should NOT have suggested search terms', function() {
          expect( _dom.suggest.isDisplayed() ).toBe( false );
        } );
      } );

      describe( 'after clicking search', function() {
        beforeEach( function() {
          _dom.trigger.click();
        } );

        it( 'should NOT have a search trigger', function() {
          // Pause to allow the transition to complete animating.
          // Update to use `protractor.until.elementIsNotVisible`
          // if this causes random failures due to differences in
          // execution time of the transition.
          browser.sleep( 500 );
          expect( _dom.trigger.isDisplayed() ).toBe( false );
        } );

        it( 'should have search input content', function() {
          expect( _dom.content.isDisplayed() ).toBe( true );
        } );

        it( 'should focus the search input field', function() {
          var activeElement = browser.driver.switchTo().activeElement();
          expect( _dom.input.getAttribute( 'id' ) )
            .toEqual( activeElement.getAttribute( 'id' ) );
        } );

        it( 'should NOT have a clear button label', function() {
          expect( _dom.clearBtn.isDisplayed() ).toBe( false );
        } );
      } );

      describe( 'after entering text', function() {
        beforeEach( function() {
          _dom.trigger.click();
          _dom.input.sendKeys( 'test' );
        } );

        it( 'should have a clear button label', function() {
          browser.wait( _dom.input.isEnabled() )
            .then( function() {
              // TODO: This test occassionally fails.
              //       Refactor to wait for the clear button longer.
              expect( _dom.clearBtn.isDisplayed() ).toBe( true );
            } );
        } );

        xit( 'should navigate to search portal', function() {

          // Wait for search button to show after expanding search.
          browser.wait( function() {
            return _dom.searchBtn.isDisplayed();
          } )
          .then( function() {
            _dom.searchBtn.click();
            var portalUrl = '/search?utf8=%E2%9C%93&affiliate=cfpb&query=test';
            expect( browser.getCurrentUrl() ).toBe( portalUrl );
          } );
        } );
      } );

      describe( 'after clicking off search', function() {
        beforeEach( function() {
          _dom.trigger.click();
          _nonLinkDom.click();
        } );

        it( 'should NOT have search input content', function() {
          // Wait for search button to disappear after collapsing search.
          var EC = protractor.ExpectedConditions;
          browser.wait(
            EC.not( EC.elementToBeClickable( _dom.content ) )
          ).then( function() {
            expect( _dom.content.isDisplayed() ).toBe( false );
          } );
        } );
      } );

      describe( 'after the tab key is pressed', function() {
        beforeEach( function() {
          _dom.trigger.sendKeys( protractor.Key.SPACE );
        } );

        it( 'should NOT have search input content', function() {
          var activeElement = browser.driver.switchTo().activeElement();
          activeElement.sendKeys( protractor.Key.TAB );
          activeElement = browser.driver.switchTo().activeElement();
          activeElement.sendKeys( protractor.Key.TAB );
          // Wait for search button to disappear after collapsing search.
          var EC = protractor.ExpectedConditions;
          browser.wait(
            EC.not( EC.elementToBeClickable( _dom.content ) )
          ).then( function() {
            expect( _dom.content.isDisplayed() ).toBe( false );
          } );
        } );
      } );
    } );
  } else if ( browser.params.windowWidth > breakpointsConfig.bpSM.min &&
              browser.params.windowWidth < breakpointsConfig.bpSM.max ) {
    describe( 'small size', function() {
      beforeEach( function() {
        _dom.trigger.click();
      } );

      it( 'should have suggested search terms', function() {
        expect( _dom.suggest.isDisplayed() ).toBe( true );
      } );
    } );
  }
} );
