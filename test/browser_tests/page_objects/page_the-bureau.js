function TheBureauPage() {
  this.get = function() {
    browser.get( '/the-bureau/' );
  };

  this.pageTitle = function() { return browser.getTitle(); };
  this.missions = element.all( by.css( '.the-bureau .mobile-carousel h1' ) );
}

module.exports = TheBureauPage;
