function Footer( url ) {
  this.get = function() {
    return browser.get( url || '/' );
  };

  this.footer = element( by.css( '.o-footer' ) );
  this.navList = this.footer.element( by.css( '.o-footer_nav-list' ) );
  this.links =
    element.all( by.css( '.o-footer_nav-list a, .o-footer-middle-left a,' +
      ' .o-footer-middle-right a, .o-footer_share-icon-list a'
    ) );
  this.post = this.footer.element( by.css( '.o-footer-post' ) );
  this.shareList = this.footer.element(
    by.css( '.o-footer_share-icon-list' )
  );
  this.officialWebsite = this.footer.element(
    by.css( '.o-footer_official-website' )
  );
}

module.exports = Footer;
