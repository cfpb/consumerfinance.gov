const { Then, When, Before } = require( 'cucumber' );
const { isShould, toCamelCase } = require( '../../util/index.js' );
const chai = require( 'chai' );
const expect = chai.expect;
const chaiAsPromised = require( 'chai-as-promised' );

const BASE_SEL = '.o-header';
const LOGO_SEL = BASE_SEL + '_logo-img';

/* Overlay is technically outside of the header,
   but makes organizational sense to include here. */
const OVERLAY_SEL = '.a-overlay';
const MEGA_MENU_SEL = BASE_SEL + ' .o-mega-menu';
const MEGA_MENU_TRIGGER_SEL = BASE_SEL + ' .o-mega-menu_trigger';
const MEGA_MENU_CONTENT_SEL = BASE_SEL + ' .o-mega-menu_content';
const GLOBAL_SEARCH_SEL = BASE_SEL + ' .m-global-search';
const GLOBAL_SEARCH_TRIGGER_SEL = BASE_SEL + ' .m-global-search_trigger';
const GLOBAL_SEARCH_CONTENT_SEL = BASE_SEL + ' .m-global-search_content';
const GLOBAL_CTA_LG_SEL = BASE_SEL + ' .m-global-header-cta';
const GLOBAL_CTA_SM_SEL = BASE_SEL +
  ' .o-mega-menu_content-1-item:first-child .o-mega-menu_content-1-link';
const GLOBAL_EYEBROW_LG_SEL = BASE_SEL + ' .m-global-eyebrow__horizontal';
const GLOBAL_EYEBROW_SM_SEL = MEGA_MENU_SEL + ' .m-global-eyebrow__list';

chai.use( chaiAsPromised );

let _dom;

Before( function() {
  _dom = {
    header:              element( by.css( BASE_SEL ) ),
    logo:                element( by.css( LOGO_SEL ) ),
    overlay:             element( by.css( OVERLAY_SEL ) ),
    megaMenu:            element( by.css( MEGA_MENU_SEL ) ),
    megaMenuTrigger:     element( by.css( MEGA_MENU_TRIGGER_SEL ) ),
    megaMenuContent:     element
      .all( by.css( MEGA_MENU_CONTENT_SEL ) )
      .first(),
    globalSearch:        element( by.css( GLOBAL_SEARCH_SEL ) ),
    globalSearchTrigger: element( by.css( GLOBAL_SEARCH_TRIGGER_SEL ) ),
    globalSearchContent: element( by.css( GLOBAL_SEARCH_CONTENT_SEL ) ),
    globalHeaderCtaLG:   element( by.css( GLOBAL_CTA_LG_SEL ) ),
    globalHeaderCtaSM:   element( by.css( GLOBAL_CTA_SM_SEL ) ),
    globalEyebrowLG:     element( by.css( GLOBAL_EYEBROW_LG_SEL ) ),
    globalEyebrowSM:     element( by.css( GLOBAL_EYEBROW_SM_SEL ) )
  };
} );

Then( /the header organism (should|shouldn't) display the (.*)/,
  function( dispayElement, element ) {

    return expect( _dom[toCamelCase( element )].isDisplayed() )
      .to.eventually
      .equal( isShould( dispayElement ) );
  }
);

When( 'I click on the mega-menu',
  function() {

    return _dom.megaMenu.click();
  }
);

When( 'I click on the mega-menu trigger',
  function() {

    return _dom.megaMenuTrigger.click();
  }
);

When( 'I click on the mega-menu search trigger', function() {

  return _dom.globalSearchTrigger.click();
} );

Then( /the mega-menu\s?(shouldn't|should)/, function( dispayElement ) {

  return expect( _dom.megaMenuContent.getAttribute( 'aria-expanded' ) )
    .to.eventually
    .equal( isShould( dispayElement ).toString() );
} );

Then( /the mega-menu search form (shouldn't|should)/,
  function( displayElement ) {

    return expect( _dom.globalSearchContent.getAttribute( 'aria-expanded' ) )
      .to.eventually
      .equal( isShould( displayElement ).toString() );
  }
);
