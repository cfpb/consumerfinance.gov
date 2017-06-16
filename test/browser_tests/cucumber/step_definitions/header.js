'use strict';

const BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';
const breakpointsConfig = require( BASE_JS_PATH + 'config/breakpoints-config' );
const { defineSupportCode } = require( 'cucumber' );
const { shouldShouldnt, toCamelCase } = require( '../../util/index.js' );

const chai = require( 'chai' );
const expect = chai.expect;
const chaiAsPromised = require( 'chai-as-promised' );

const BASE_SEL = '.o-header';
const LOGO_SEL = BASE_SEL + '_logo-img';

// Overlay is technically outside of the header,
// but makes organizational sense to include here.
const OVERLAY_SEL = '.a-overlay';
const MEGA_MENU_SEL = BASE_SEL + ' .o-mega-menu';
const MEGA_MENU_TRIGGER_SEL = BASE_SEL + ' .o-mega-menu_trigger';
const MEGA_MENU_CONTENT_SEL = BASE_SEL + ' .o-mega-menu_content';
const GLOBAL_SEARCH_SEL = BASE_SEL + ' .m-global-search';
const GLOBAL_SEARCH_TRIGGER_SEL = BASE_SEL + ' .m-global-search_trigger';
const GLOBAL_SEARCH_CONTENT_SEL = BASE_SEL + ' .m-global-search_content';
const GLOBAL_CTA_LG_SEL = BASE_SEL + ' .m-global-header-cta__horizontal';
const GLOBAL_CTA_SM_SEL = BASE_SEL + ' .m-global-header-cta__list';
const GLOBAL_EYEBROW_LG_SEL = BASE_SEL + ' .m-global-eyebrow__horizontal';
const GLOBAL_EYEBROW_SM_SEL = MEGA_MENU_SEL + ' .m-global-eyebrow__list';
const EC = protractor.ExpectedConditions;


chai.use( chaiAsPromised );

let _dom;

defineSupportCode( function( { Then, When, Before } ) {

  Before( function() {
    _dom = {
      header:              element( by.css( BASE_SEL ) ),
      logo:                element( by.css( LOGO_SEL ) ),
      overlay:             element( by.css( OVERLAY_SEL ) ),
      megaMenu:            element( by.css( MEGA_MENU_SEL ) ),
      megaMenuTrigger:     element( by.css( MEGA_MENU_TRIGGER_SEL ) ),
      megaMenuContent:     element.all( by.css( MEGA_MENU_CONTENT_SEL ) ).first(),
      globalSearch:        element( by.css( GLOBAL_SEARCH_SEL ) ),
      globalSearchTrigger: element( by.css( GLOBAL_SEARCH_TRIGGER_SEL ) ),
      globalSearchContent: element( by.css( GLOBAL_SEARCH_CONTENT_SEL ) ),
      globalHeaderCtaLG:   element( by.css( GLOBAL_CTA_LG_SEL ) ),
      globalHeaderCtaSM:   element( by.css( GLOBAL_CTA_SM_SEL ) ),
      globalEyebrowLG:     element( by.css( GLOBAL_EYEBROW_LG_SEL ) ),
      globalEyebrowSM:     element( by.css( GLOBAL_EYEBROW_SM_SEL ) )
    };

    const script = 'document.body.className = "u-move-transition__disabled";';

    browser.executeScript( script );
  } );

  Then( /the header organism (should|shouldn't) display the (.*)/,
    function( shouldDispayElement, element ) {

      return expect( _dom[toCamelCase( element )].isDisplayed() )
             .to.eventually
             .to.equal( shouldShouldnt( shouldDispayElement ) );
    }
  );

  When( 'I click on the mega-menu',
    function( ) {

      return browser
             .wait( EC.elementToBeClickable( _dom.megaMenu ) )
             .then( _dom.megaMenu.click );
    }
  );

  When( 'I click the the mega-menu trigger',
    function( ) {

      return  browser
              .wait( EC.elementToBeClickable( _dom.megaMenuTrigger ) )
              .then( _dom.megaMenuTrigger.click );
    }
  );

  When( 'I click on search', function() {
    _dom.megaMenuTrigger.click();

    return _dom.globalSearchTrigger.click();
  } );

  Then( 'it should show the search and hide megamenu', function() {
    expect( _dom.globalSearchContent.getAttribute( 'aria-expanded' ) )
    .to.eventually
    .to.equal( 'true' );

    return expect( _dom.megaMenuContent.getAttribute( 'aria-expanded' ) )
           .to.eventually
           .to.equal( 'false' );
  } );

  Then( 'it should show the mega menu and hide search', function() {

    // Since the code doesn't work when .u-move-transition__disabled is
    // set to 0ms, we still need a quick sleep.
    browser.sleep( 2 );

    expect( _dom.megaMenuContent.getAttribute( 'aria-expanded' ) )
    .to.eventually
    .equal( 'true' );

    return expect( _dom.globalSearchContent.getAttribute( 'aria-expanded' ) )
           .to.eventually
           .equal( 'false' );
  } );

} );
