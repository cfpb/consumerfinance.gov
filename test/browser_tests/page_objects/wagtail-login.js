'use strict';

function WagtailLogin() {

  this.gotoURL = function( url='/admin' ) {
    browser.get( url );
  };

  this.enterLoginCriteria = function( ) {
    this.userName.sendKeys( 'admin' );
    this.userPassword.sendKeys( 'password' );
  };

  this.userName = element( by.css( '#id_username' ) );

  this.userPassword = element( by.css( '#id_password' ) );

  this.loginBtn = element( by.css( 'button' ) );
}

module.exports = WagtailLogin;
