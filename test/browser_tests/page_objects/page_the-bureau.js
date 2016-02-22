'use strict';

function TheBureauPage() {
  this.get = function() {
    browser.get( '/the-bureau/' );
  };

  this.pageTitle = function() { return browser.getTitle(); };

  this.sideNav = element( by.css( '.o-secondary-navigation' ) );

  this.hero = element( by.css( '.hero' ) );

  this.bureauHistory = element( by.css( '.bureau-history' ) );

  this.bureauMission =
  element.all( by.css( '.js-mobile-carousel .media-stack_item' ) );

  this.bureauFunctions =
  element( by.css( '[data-qa-hook="bureau-core-functions"]' ) );

  this.directorsBio = element.all( by.css( '.bureau-bio' ) ).first();

  this.directorsName =
  this.directorsBio.element( by.css( '.bureau-bio_name' ) );

  this.deputyDirectorsBio = element.all( by.css( '.bureau-bio' ) ).last();

  this.deputyDirectorsName =
  this.deputyDirectorsBio.element( by.css( '.bureau-bio_name' ) );
}

module.exports = TheBureauPage;
