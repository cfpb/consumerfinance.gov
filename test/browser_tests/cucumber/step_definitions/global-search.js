const chai = require( 'chai' );
const chaiAsPromised = require( 'chai-as-promised' );
const { Then, When, Before } = require( '@cucumber/cucumber' );
const { expect } = require( 'chai' );
const { isShould } = require( '../../util/index.js' );

const BASE_SEL = '.m-global-search';
const TRIGGER_SEL = BASE_SEL + ' [data-js-hook="behavior_flyout-menu_trigger"]';
const CONTENT_SEL = BASE_SEL + ' [data-js-hook="behavior_flyout-menu_content"]';
const INPUT_SEL = BASE_SEL + ' input#m-global-search_query';
const SEARCH_SEL = BASE_SEL +
  ' [data-js-hook="behavior_flyout-menu_content"] .a-btn';
const SUGGEST_SEL = BASE_SEL + ' .m-global-search_content-suggestions';
const EC = protractor.ExpectedConditions;

let _dom;
let _nonLinkDom;

chai.use( chaiAsPromised );

Before( function() {
  _nonLinkDom = element( by.css( '.o-footer .a-tagline' ) );
  _dom = {
    trigger:   element( by.css( TRIGGER_SEL ) ),
    content:   element( by.css( CONTENT_SEL ) ),
    input:     element( by.css( INPUT_SEL ) ),
    searchBtn: element( by.css( SEARCH_SEL ) ),
    suggest:   element( by.css( SUGGEST_SEL ) )
  };
} );

When( 'I click on the search molecule',
  function() {

    return _dom.trigger.click();
  }
);

When( /I enter "(.*)" in the search molecule/,
  async function( searchText ) {
    await _dom.trigger.click();

    return _dom.input.sendKeys( searchText );
  }
);

When( 'I click off the search molecule',
  async function() {
    await _dom.trigger.click();
    await browser.wait( EC.visibilityOf( _dom.input ) );

    return _nonLinkDom.click();
  }
);

When( 'I focus on the search molecule trigger',
  function() {

    return _dom.trigger.sendKeys( protractor.Key.SPACE );
  }
);

When( 'I perform tab actions on the search molecule',
  async function() {
    let activeElement = await browser.driver.switchTo().activeElement();
    await activeElement.sendKeys( protractor.Key.TAB );
    activeElement = await browser.driver.switchTo().activeElement();

    return activeElement.sendKeys( protractor.Key.TAB );
  }
);

Then( 'it should focus the search input field',
  async function() {
    const attributeId = await browser
      .driver
      .switchTo()
      .activeElement()
      .getAttribute( 'id' );

    return expect( _dom.input.getAttribute( 'id' ) )
      .to.eventually.equal( attributeId );
  }
);

Then( /the search molecule (should|shouldn't) have a search trigger/,
  async function( haveTrigger ) {
    let expectedCondition;

    if ( isShould( haveTrigger ) ) {
      expectedCondition =
        await EC.elementToBeClickable( _dom.trigger );
    } else {
      expectedCondition =
        await EC.not( EC.elementToBeClickable( _dom.trigger ) );
    }

    await browser.wait( expectedCondition );

    return expect( _dom.trigger.isDisplayed() )
      .to.eventually
      .equal( isShould( haveTrigger ) );
  }
);

Then( /it (should|shouldn't) have search input content/,
  async function( haveInput ) {
    await browser.sleep( 300 );

    return expect( _dom.content.isDisplayed() )
      .to.eventually
      .equal( isShould( haveInput ) );
  }
);

Then( 'I should navigate to search portal',
  async function() {
    const portalUrl = 'https://search.consumerfinance.gov/' +
                      'search?utf8=%E2%9C%93&affiliate=cfpb&query=test';

    await browser.wait( EC.visibilityOf( _dom.searchBtn ) );
    await _dom.searchBtn.click();

    return expect( browser.getCurrentUrl().then( url => {
      url.substring( 0, url.lastIndexOf( '&' ) )
        .to.eventually
        .equal( portalUrl );
    } ) );
  }
);

Then( /it (should|shouldn't) have suggested search terms/,
  function( haveTerms ) {

    return expect( _dom.suggest.isDisplayed() )
      .to.eventually
      .equal( isShould( haveTerms ) );
  }
);

Then( 'should have suggested search terms',
  function() {

    return expect( _dom.suggest.isDisplayed() )
      .to.eventually
      .equal( true );
  }
);
