const BasePage = require( '../../page_objects/base-page.js' );
const basePage = new BasePage();

const { defineSupportCode } = require( 'cucumber' );
const { expect } = require( 'chai' );

defineSupportCode( function( { Then, When } ) {

  When( /I goto URL "(.*)"/, { timeout: 60 * 1000 }, function( url ) {
    return basePage.gotoURL( url ).then( function() {
      return expect( browser.getCurrentUrl() ).to.eventually.contain( url );
    } );
  } );

  When( /I navigate back*/, function() {

    return browser.navigate().back();
  } );

  When( /I click away*/, function() {

    return element( by.css( 'body' ) ).click( );
  } );

  Then( /I should see page title "(.*)"/, function( pageTitle ) {

    return browser.getTitle().then( function( title ) {

      return expect( title ).to.equal( pageTitle );
    } );
  } );

} );
