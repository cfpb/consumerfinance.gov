'use strict';

function Header() {
  this.get = function() {
    browser.get( '/' );
  };

  this.header = element( by.css( '.header' ) );
  this.logo = element( by.css( '.header_logo' ) );
  this.navList = element( by.css( '.primary-nav' ) );
  this.primaryLinks = element.all( by.css( '.primary-nav_link' ) );
  this.subLinks = element.all( by.css( '.sub-nav_link' ) );
}

module.exports = Header;
