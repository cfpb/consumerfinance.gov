'use strict';

function AboutUs() {
  this.get = function() {
    browser.get( '/about-us/' );
  };

  this.pageTitle = function() { return browser.getTitle(); };
  this.activityBlock = element.all( by.css( '.activity' ) );
  this.feedIcons = element.all( by.css( '.activity h1 .cf-icon' ) );
  this.firstIcon = this.feedIcons.first();
  this.secondIcon = this.feedIcons.last();
}

module.exports = AboutUs;
