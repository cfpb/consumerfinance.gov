'use strict';

var WagtailLogin = require( '../../page_objects/wagtail-login-page.js' );
var wagtailLoginPage  = new WagtailLogin();

var {defineSupportCode} = require('cucumber');
var {expect} = require('chai');

defineSupportCode( function( { Then, When } ) {
  When( 'I goto /login', function () {
   	wagtailLoginPage.gotoURL();
  } );

  When( 'I enter my login criteria', function() {
    wagtailLoginPage.enterLoginCriteria();
  } );

  When( 'I am logged into Wagtail as an admin', function() {
    wagtailLoginPage.login();
  } );

  When( 'I should be able to access the admin section', function () {
    wagtailLoginPage.clickloginBtn();

  	return browser.getCurrentUrl()
           .then( function( url ) {
  		        expect( url ).to.contain( '/login/welcome' );
  	       } );
  } );
} );
