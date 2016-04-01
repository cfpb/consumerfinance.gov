'use strict';

var BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';

var breakpointsConfig = require( BASE_JS_PATH + 'config/breakpoints-config' );

describe( 'Header', function() {
  var BASE_SEL = '.o-header';
  var LOGO_SEL = BASE_SEL + '_logo-img';
  var MEGA_MENU_SEL = BASE_SEL + ' .o-mega-menu';
  var GLOBAL_SEARCH_SEL = BASE_SEL + ' .m-global-search';
  var GLOBAL_CTA_LG_SEL = BASE_SEL + ' .m-global-header-cta__horizontal';
  var GLOBAL_CTA_SM_SEL = BASE_SEL + ' .m-global-header-cta__list';
  var GLOBAL_EYEBROW_LG_SEL = BASE_SEL + ' .m-global-eyebrow__horizontal';
  var GLOBAL_EYEBROW_SM_SEL = MEGA_MENU_SEL + ' .m-global-eyebrow__list';

  var _dom;

  beforeAll( function() {
    _dom = {
      header:            element( by.css( BASE_SEL ) ),
      logo:              element( by.css( LOGO_SEL ) ),
      megaMenu:          element( by.css( MEGA_MENU_SEL ) ),
      globalSearch:      element( by.css( GLOBAL_SEARCH_SEL ) ),
      globalHeaderCtaLG: element( by.css( GLOBAL_CTA_LG_SEL ) ),
      globalHeaderCtaSM: element( by.css( GLOBAL_CTA_SM_SEL ) ),
      globalEyebrowLG:   element( by.css( GLOBAL_EYEBROW_LG_SEL ) ),
      globalEyebrowSM:   element( by.css( GLOBAL_EYEBROW_SM_SEL ) )
    };
  } );

  beforeEach( function() {
    browser.get( '/' );
  } );

  if ( browser.params.windowWidth > breakpointsConfig.bpLG.min ) {
    describe( 'large size', function() {
      describe( 'at page load', function() {
        it( 'should display Header', function() {
          expect( _dom.header.isDisplayed() ).toBe( true );
        } );

        it( 'should display logo', function() {
          expect( _dom.logo.isDisplayed() ).toBe( true );
        } );

        it( 'should display Mega Menu', function() {
          expect( _dom.megaMenu.isDisplayed() ).toBe( true );
        } );

        it( 'should display Global Search', function() {
          expect( _dom.globalSearch.isDisplayed() ).toBe( true );
        } );

        it( 'should display large Global Header CTA', function() {
          expect( _dom.globalHeaderCtaLG.isDisplayed() ).toBe( true );
        } );

        it( 'should NOT display small Global Header CTA', function() {
          expect( _dom.globalHeaderCtaSM.isDisplayed() ).toBe( false );
        } );

        it( 'should display large Global Eyebrow', function() {
          expect( _dom.globalEyebrowLG.isDisplayed() ).toBe( true );
        } );

        it( 'should NOT display small Global Eyebrow', function() {
          expect( _dom.globalEyebrowSM.isDisplayed() ).toBe( false );
        } );
      } );
    } );
  } else if ( browser.params.windowWidth > breakpointsConfig.bpSM.min &&
              browser.params.windowWidth < breakpointsConfig.bpSM.max ) {
    describe( 'small size', function() {
      describe( 'at page load', function() {
        it( 'should display Header', function() {
          expect( _dom.header.isDisplayed() ).toBe( true );
        } );

        it( 'should display logo', function() {
          expect( _dom.logo.isDisplayed() ).toBe( true );
        } );

        it( 'should display Mega Menu', function() {
          expect( _dom.megaMenu.isDisplayed() ).toBe( true );
        } );

        it( 'should display Global Search', function() {
          expect( _dom.globalSearch.isDisplayed() ).toBe( true );
        } );

        it( 'should NOT display large Global Header CTA', function() {
          expect( _dom.globalHeaderCtaLG.isDisplayed() ).toBe( false );
        } );

        xit( 'should display small Global Header CTA', function() {
          // TODO: Click mega menu to show Global Header CTA.
          //       Or move this to the mega menu test.
          expect( _dom.globalHeaderCtaSM.isDisplayed() ).toBe( true );
        } );

        it( 'should NOT display large Global Eyebrow', function() {
          expect( _dom.globalEyebrowLG.isDisplayed() ).toBe( false );
        } );

        xit( 'should display small Global Eyebrow', function() {
          // TODO: Click mega menu to show Global Eyebrow.
          //       Or move this to the mega menu test.
          expect( _dom.globalEyebrowSM.isDisplayed() ).toBe( true );
        } );
      } );

      // TODO: Add tests for clicking between menu and search.
      // describe( 'click search when mega menu is showing', function() {} );
      // describe( 'click mega menu when search is showing', function() {} );
    } );
  }
} );
