'use strict';

var BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';

var breakpointsConfig = require( BASE_JS_PATH + 'config/breakpoints-config' );

describe( 'MegaMenu', function() {
  var BASE_SEL = '.o-mega-menu';
  var TRIGGER_1_SEL = BASE_SEL + '_content-1-link';
  var CONTENT_2_SEL = BASE_SEL + '_content-2';

  var _dom;

  // Check large size.
  if ( browser.params.windowWidth > breakpointsConfig.bpLG.min ) {
    describe( 'large size', function() {

      beforeAll( function() {
        _dom = {
          triggerPolyCom: element.all( by.css( TRIGGER_1_SEL ) ).get( 3 ),
          triggerAboutUs: element.all( by.css( TRIGGER_1_SEL ) ).get( 4 ),
          contentPolyCom: element.all( by.css( CONTENT_2_SEL ) ).get( 3 ),
          contentAboutUs: element.all( by.css( CONTENT_2_SEL ) ).get( 4 )
        };
      } );

      beforeEach( function() {
        browser.get( '/' );
      } );

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
          // Wait for delay to show menu
          browser.sleep( 500 );
          browser.driver.actions().mouseMove( _dom.triggerAboutUs ).perform();
        } );

        it( 'should ONLY show second link content', function() {
          // TODO: Look up contentPolyCom to pass to elementIsNotVisible().
          //       It would be nice to be able to _dom.contentPolyCom.
          //       Investigate having only _dom.contentPolyCom.
          var elem;
          browser.driver.findElements( by.css( CONTENT_2_SEL ) )
            .then( function( value ) {
              // PolyCom content.
              elem = value[3];

              browser.wait(
                protractor.until.elementIsNotVisible( elem )
              ).then( function() {
                expect( _dom.contentPolyCom.isDisplayed() ).toBe( false );
                expect( _dom.contentAboutUs.isDisplayed() ).toBe( true );
              } );
            } );
        } );
      } );

      // TODO: Add test for:
      //       - Moving over and off the menu.
      //       - Clicking the menu link.
      //       - Tabbing over the menu.
    } );
  }
} );
