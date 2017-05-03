'use strict';

var BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';

var Wagtail = require( '../../page_objects/wagtail.js' );

var page  = new Wagtail();

describe( 'Wagtail', function() {

  beforeEach( function() {
    page.login();

  } );

  describe( 'on page load', function() {
    it( 'should create the multiselect', function() {
      page.userName.sendKeys( 'admin' );
      page.userPassword.sendKeys( 'password' );
      page.loginBtn.click();
    } );
  } );

} );
