const { Then, When, Before } = require( '@cucumber/cucumber' );
const chai = require( 'chai' );
const expect = chai.expect;
const chaiAsPromised = require( 'chai-as-promised' );

const BASE_SEL = '.o-mega-menu';
const TRIGGER_BTN = '.o-mega-menu_trigger';
const CONTENT_WRAPPER = '.o-mega-menu_content';
const EYEBROW = '.m-global-eyebrow_tagline';
const TRIGGER_1_SEL = BASE_SEL + '_content-1-link';
const CONTENT_2_SEL = BASE_SEL + '_content-2';
const EC = protractor.ExpectedConditions;

chai.use( chaiAsPromised );

let _dom;

Before( function() {
  _dom = {
    triggerBtn:     element( by.css( TRIGGER_BTN ) ),
    contentWrapper: element( by.css( CONTENT_WRAPPER ) ),
    eyebrow:        element( by.css( EYEBROW ) ),
    triggerFourthMenuItem: element.all( by.css( TRIGGER_1_SEL ) ).get( 3 ),
    triggerFifthMenuItem: element.all( by.css( TRIGGER_1_SEL ) ).get( 4 ),
    contentFourthMenuItem: element.all( by.css( CONTENT_2_SEL ) ).get( 3 ),
    contentFifthMenuItem: element.all( by.css( CONTENT_2_SEL ) ).get( 4 )
  };
} );

When( 'mouse moves from one link to another',
  async function() {
    await browser.actions()
      .mouseMove( _dom.triggerFourthMenuItem ).perform();

    return browser.actions()
      .mouseMove( _dom.triggerFifthMenuItem ).perform();
  }
);

Then( 'the mega-menu organism should not show content', function() {

  return expect( _dom.contentFifthMenuItem.isDisplayed() )
    .to.eventually.equal( false );
} );

Then( 'should only show second link content', async function() {
  await EC.not( EC.elementToBeClickable( _dom.contentFourthMenuItem ) );
  await browser.sleep( 500 );


  await expect( _dom.contentFourthMenuItem.isDisplayed() )
    .to.eventually.equal( false );

  return expect( _dom.contentFourthMenuItem.isDisplayed() )
    .to.eventually.equal( false );
} );

Then( 'the mega-menu organism should show menu when clicked',
  async function() {
    await browser.driver.actions().click( _dom.triggerBtn ).perform();

    return expect( _dom.contentWrapper.isDisplayed() )
      .to.eventually.equal( true );
  }
);

Then( 'the mega-menu organism should show the FourthMenuItem menu when clicked',
  async function() {
    await browser.driver.actions()
      .click( _dom.triggerBtn ).perform();
    await browser.driver.actions()
      .click( _dom.triggerFourthMenuItem ).perform();
    await expect( _dom.contentFourthMenuItem.isDisplayed() )
      .to.eventually.equal( true );

    return expect( _dom.contentFifthMenuItem.isDisplayed() )
      .to.eventually.equal( false );
  }
);

/* This test is failing right now, but should pass
   when we fix keyboard tabbing on mobile */
Then( 'the mega-menu organism should not shift menus when tabbing',
  async function() {
    await browser.driver.actions().click( _dom.triggerBtn ).perform();
    await browser.driver.actions().sendKeys( protractor.Key.TAB ).perform();
    await browser.driver.actions().sendKeys( protractor.Key.TAB ).perform();
    await browser.driver.actions().sendKeys( protractor.Key.TAB ).perform();
    await browser.driver.actions().sendKeys( protractor.Key.TAB ).perform();

    return expect( _dom.eyebrow.isDisplayed() ).to.eventually.equal( false );
  }
);
