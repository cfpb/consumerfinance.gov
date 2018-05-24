const BasePage = require( '../../page_objects/base-page.js' );
const basePage = new BasePage();

const { Then, When } = require( 'cucumber' );
const { expect } = require( 'chai' );

When( /I goto URL "(.*)"/, { timeout: 60 * 1000 }, async function( url ) {
  await basePage.gotoURL( url );

  return expect( browser.getCurrentUrl() ).to.eventually.contain( url );
} );

When( /I navigate back*/, function() {

  return browser.navigate().back();
} );

When( /I click away*/, function() {

  return element( by.css( 'body' ) ).click();
} );

Then( /I should see page title "(.*)"/, async function( pageTitle ) {
  const title = await browser.getTitle();

  return expect( title ).to.equal( pageTitle );
} );
