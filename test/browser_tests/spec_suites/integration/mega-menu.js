'use strict';

var BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';

var breakpointsConfig = require( BASE_JS_PATH + 'config/breakpoints-config' );

describe( 'MegaMenu', function() {
  var BASE_SEL = '.o-mega-menu';
  var TRIGGER_BTN = '.o-mega-menu_trigger';
  var CONTENT_WRAPPER = '.o-mega-menu_content';
  var EYEBROW = '.m-global-eyebrow_tagline';
  var TRIGGER_1_SEL = BASE_SEL + '_content-1-link';
  var CONTENT_2_SEL = BASE_SEL + '_content-2';

  var _dom;

  beforeAll( function() {
    _dom = {
      triggerBtn:     element( by.css( TRIGGER_BTN ) ),
      contentWrapper: element( by.css( CONTENT_WRAPPER ) ),
      eyebrow:        element( by.css( EYEBROW ) ),
      triggerPolyCom: element.all( by.css( TRIGGER_1_SEL ) ).get( 3 ),
      triggerAboutUs: element.all( by.css( TRIGGER_1_SEL ) ).get( 4 ),
      contentPolyCom: element.all( by.css( CONTENT_2_SEL ) ).get( 3 ),
      contentAboutUs: element.all( by.css( CONTENT_2_SEL ) ).get( 4 )
    };
  } );

  beforeEach( function() {
    browser.get( '/' );
  } );

  // Check large size.
  if ( browser.params.windowWidth > breakpointsConfig.bpLG.min ) {
    describe( 'large size', function() {

      describe( 'at page load', function() {
        it( 'should NOT show content', function() {
          expect( _dom.contentAboutUs.isDisplayed() ).toBe( false );
        } );
      } );

      describe( 'when mouse is over link', function() {
        it( 'should NOT show first link content immediately', function() {
          browser.driver.actions().mouseMove( _dom.triggerPolyCom ).perform()
            .then( function() {
              expect( _dom.contentPolyCom.isDisplayed() ).toBe( false );
            } );
        } );

        it( 'should show first link content after a delay', function() {
          browser.driver.actions().mouseMove( _dom.triggerPolyCom ).perform()
            .then( function() {
              // Wait for delay to show menu
              browser.sleep( 500 );
              expect( _dom.contentPolyCom.isDisplayed() ).toBe( true );
            } );
        } );
      } );

      describe( 'when mouse moves from one link ' +
                'to another after a delay', function() {
        beforeEach( function() {
          browser.driver.actions().mouseMove( _dom.triggerPolyCom ).perform();
          // The menu has a built-in delay before it expands.
          // This waits for that delay.
          browser.sleep( 500 );
          browser.driver.actions().mouseMove( _dom.triggerAboutUs ).perform();
        } );

        it( 'should ONLY show second link content', function() {
          var EC = protractor.ExpectedConditions;
          browser.wait(
            EC.not( EC.elementToBeClickable( _dom.contentPolyCom ) )
          ).then( function() {
            expect( _dom.contentPolyCom.isDisplayed() ).toBe( false );
            expect( _dom.contentAboutUs.isDisplayed() ).toBe( true );
          } );
        } );
      } );
    } );
  } else if ( browser.params.windowWidth < breakpointsConfig.bpSM.max ) {

    describe( 'mobile size', function() {
      it( 'should show menu when clicked', function() {
        browser.driver.actions().click( _dom.triggerBtn ).perform()
          .then( function() {
            expect( _dom.contentWrapper.isDisplayed() ).toBe( true );
          } );
      } );

      it( 'should show the PolyCom menu when clicked', function() {
        browser.driver.actions().click( _dom.triggerBtn ).perform();
        browser.sleep( 500 );
        browser.driver.actions().click( _dom.triggerPolyCom ).perform()
          .then( function() {
            expect( _dom.contentPolyCom.isDisplayed() ).toBe( true );
            expect( _dom.contentAboutUs.isDisplayed() ).toBe( false );
          } );
      } );

      // This test is failing right now, but should pass
      // when we fix keyboard tabbing on mobile
      xit( 'should not shift menus when tabbing', function() {
        browser.driver.actions().click( _dom.triggerBtn ).perform();
        browser.driver.actions().sendKeys( protractor.Key.TAB ).perform();
        browser.driver.actions().sendKeys( protractor.Key.TAB ).perform();
        browser.driver.actions().sendKeys( protractor.Key.TAB ).perform();
        browser.driver.actions().sendKeys( protractor.Key.TAB ).perform();
        expect( _dom.eyebrow.isDisplayed() ).toBe( true );
      } );
    } );
  }
} );
