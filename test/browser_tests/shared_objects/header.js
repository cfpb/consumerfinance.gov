'use strict';

function Header( url ) {
  this.get = function() {
    browser.get( url || '/' );
  };

  this.header = element( by.css( '.o-header' ) );
  this.logo = element( by.css( '.o-header_logo-img' ) );
  this.navList = element( by.css( '.o-mega-menu_content-1-lists' ) );
  this.primaryLinks =
    this.navList.all( by.css( '.o-mega-menu_content-1-item' ) );
  this.subLinks = element.all( by.css( '.o-mega-menu_content-2-link' ) );
}

module.exports = Header;
