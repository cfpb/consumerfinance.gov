'use strict';

var _getQAElement = require( '../util/qa-element' ).get;

function Wagtail() {

  this.login = function( page ) {
    browser.get( '/admin' );
  };

  this.userName = element( by.css( '#id_username' ) );

  this.userPassword = element( by.css( '#id_password' ) );

  this.loginBtn = element( by.css( 'button' ) );

}

module.exports = Wagtail;
