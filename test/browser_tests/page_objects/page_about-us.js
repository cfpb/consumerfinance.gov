'use strict';

function AboutUs() {
  this.get = function() {
    browser.get( '/about-us/' );
  };

  this.pageTitle = function() { return browser.getTitle(); };
  this.activityBlock = element.all( by.css( '.activity' ) );
  this.feedIcons = element.all( by.css( '.activity .cf-icon' ) );
  this.firstIcon = this.feedIcons.first();
  this.secondIcon = this.feedIcons.last();
  this.activityItems = element.all( by.css( '.activity .list-item' ) );
}

module.exports = AboutUs;
