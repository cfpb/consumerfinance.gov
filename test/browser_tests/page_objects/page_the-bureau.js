'use strict';

function TheBureauPage() {
  this.get = function() {
    browser.get( '/the-bureau/' );
  };

  this.pageTitle = function() { return browser.getTitle(); };

  this.sideNav = element( by.css( '.o-secondary-navigation' ) );

  this.bureauFunctions =
  element( by.css( '[data-qa-hook="bureau-core-functions"]' ) );
}

module.exports = TheBureauPage;
