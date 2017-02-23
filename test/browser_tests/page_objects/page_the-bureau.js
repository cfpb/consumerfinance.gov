'use strict';

var secondaryNav = require( '../shared_objects/secondary-navigation' );
var videoPlayer = require( '../shared_objects/video-player' );

function TheBureauPage() {
  Object.assign( this, secondaryNav, videoPlayer );

  this.get = function() {
    browser.get( '/about-us/the-bureau/' );
  };

  this.pageTitle = function() { return browser.getTitle(); };

  this.bureauFunctions =
  element( by.css( '[data-qa-hook="bureau-core-functions"]' ) );
}

module.exports = TheBureauPage;
