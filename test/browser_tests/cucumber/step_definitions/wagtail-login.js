'use strict';

var BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';

var WagtailLogin = require( '../../page_objects/wagtail-login.js' );
var wagtailLoginPage  = new WagtailLogin();

var {defineSupportCode} = require('cucumber');
var {expect} = require('chai');

defineSupportCode( function( { Then, When } ) {
  When( 'I goto /login', function () {
   	wagtailLoginPage.gotoURL();
  } );

  When( 'I enter my login criteria', function ( ) {
   	wagtailLoginPage.enterLoginCriteria();
  } );

  When( 'I should be able to access the admin section', function ( ) {
    wagtailLoginPage.loginBtn.click();

  	return browser.getCurrentUrl().then( function( url ) {
  		expect( url ).to.contain( '/admin' )
  	} )
  } );
} );
