'use strict';

function AboutUs() {
  this.get = function() {
    browser.get( '/about-us/' );
  };

  this.pageTitle = function() { return browser.getTitle(); };
  this.sidebar = element.all( by.css( 'aside.activity' ) );
  this.feedIcons = element.all( by.css( 'aside.activity h1 .cf-icon' ) );
}

module.exports = AboutUs;
