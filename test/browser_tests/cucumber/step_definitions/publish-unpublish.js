'use strict';

const BasePage = require('../../page_objects/base-page.js');
const basePage = new BasePage();

const { defineSupportCode } = require( 'cucumber' );
const { expect } = require( 'chai' );

defineSupportCode( function( { Then, When } ) {

  When( /I visit URL "(.*)"/, function( url ) {
    return basePage.gotoURL( url );
  } );

  When( 'I navigate back to the edit page', function( ) {
    return browser.navigate().back();
  } );

  Then( /I should see page title "(.*)"/, function( pageTitle ) {
    return browser.getTitle().then( function(title) {
      expect( title ).to.equal( pageTitle );
    } );
  } );

} );
