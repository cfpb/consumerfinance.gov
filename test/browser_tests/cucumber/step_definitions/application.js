const BasePage = require( '../../page_objects/base-page.js' );
const basePage = new BasePage();

const { Then, When } = require( 'cucumber' );
const { expect } = require( 'chai' );

When( /I goto URL "(.*)"/, { timeout: 60 * 1000 }, async function( url ) {
  await basePage.gotoURL( url );

  return expect( browser.getCurrentUrl() ).to.eventually.contain( url );
} );

When( /I go to redirecting URL "(.*)"/, { timeout: 60 * 1000 }, async function( url ) {
  await basePage.gotoURL( url );

  return expect( browser.getCurrentUrl() ).to.eventually.not.contain( url );
} );

Then( /I should be redirected to URL "(.+)"/, async function( url ) {
  const currentURL = await browser.getCurrentUrl();
  const regex = new RegExp( url );
  return expect( currentURL ).to.match( regex );
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
