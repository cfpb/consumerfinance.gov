const WagtailLogin = require(
  '../../page_objects/wagtail-admin-login-page.js'
);
const wagtailLoginPage = new WagtailLogin();
const { defineSupportCode } = require( 'cucumber' );
const { expect } = require( 'chai' );

defineSupportCode( function( { Then, When, Given } ) {

  Given( 'I am logged into Wagtail as an admin', function() {

    return wagtailLoginPage.login();
  } );

  When( 'I goto /login', function() {

    return wagtailLoginPage.gotoURL();
  } );

  When( 'I enter my login criteria', function() {

    return wagtailLoginPage.enterLoginCriteria();
  } );

  When( 'I click the login button', function() {

    return wagtailLoginPage.clickLoginBtn( );
  } );

  Then( 'I should be able to access the admin section', function() {

    return browser.getCurrentUrl().then( function( url ) {
      expect( url ).to.contain( '/admin' );
    } );
  } );

} );
