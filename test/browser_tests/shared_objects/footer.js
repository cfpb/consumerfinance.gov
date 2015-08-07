'use strict';

function Footer() {
  this.get = function() {
    browser.get( '/' );
  };

  this.footer = element( by.css( '.footer' ) );
  this.navList = this.footer.element( by.css( '.footer_nav-list' ) );
  this.links =
  element.all( by.css( '.footer_nav-list a, .footer-middle-left a,' +
    ' .footer-middle-right a, .footer_share-icon-list a'
  ) );
  this.post = this.footer.element( by.css( '.footer-post' ) );
  this.shareList = this.footer.element( by.css( '.footer_share-icon-list' ) );
  this.officialWebsite = this.footer.element(
    by.css( '.footer_official-website' )
  );
}

module.exports = Footer;
