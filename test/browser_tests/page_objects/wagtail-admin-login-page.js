const BasePage = require( './base-page.js' );
const USERS = require( '../util/wagtail-admin-users.js' );


class WagtailLoginPage extends BasePage {

  constructor() {
    super();
    this.userName = element( by.css( '#id_username' ) );
    this.userPassword = element( by.css( '#id_password' ) );
    this.loginBtn = element( by.css( 'button' ) );
    this.URL = '/admin';
  }

  enterLoginCriteria( USER = USERS.ADMIN ) {
    this.userName.sendKeys( USER.USERNAME );

    return this.userPassword.sendKeys( USER.PASSWORD );
  }

  clickLoginBtn() {

    return this.loginBtn.click();
  }

  login( USER = USERS.ADMIN ) {
    const _this = this;

    function _login( url ) {
      if ( url.indexOf( '/login' ) > -1 ) {
        _this.enterLoginCriteria( USER );

        return _this.clickLoginBtn();
      }

      return Promise.resolve();
    }

    return this.gotoURL()
      .then( browser.getCurrentUrl )
      .then( _login );
  }

}

WagtailLoginPage.USERS = USERS;

module.exports = WagtailLoginPage;
