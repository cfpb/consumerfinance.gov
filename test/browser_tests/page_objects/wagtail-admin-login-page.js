'use strict';

let BasePage = require( './wagtail-admin-base-page.js' );

class WagtailLoginPage extends BasePage {

  constructor() {
    super();
    this.userName = element( by.css( '#id_username' ) );
    this.userPassword = element( by.css( '#id_password' ) );
    this.loginBtn = element( by.css( 'button' ) );
    this.URL = '/admin';
  }

  enterLoginCriteria() {
    this.userName.sendKeys( 'admin' );

    return this.userPassword
           .sendKeys( 'password' );
  }

  clickloginBtn() {

    return this.loginBtn.click();
  }

  login() {
    var _this = this;

    function _login( url ) {
      if ( url.indexOf( '/login' ) > -1 ) {
        _this.enterLoginCriteria();

        return _this.clickloginBtn();
      }

      return Promise.resolve();
    }

    return this.gotoURL()
           .then( browser.getCurrentUrl )
           .then( _login );
  }

}

module.exports = WagtailLoginPage;
