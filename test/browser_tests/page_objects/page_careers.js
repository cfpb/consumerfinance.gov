'use strict';

var _getQAelement = require( '../util/qa-element' ).get;

function Careers() {

  this.get = function() {
    browser.get( '/about-us/careers/' );
  };

  this.pageTitle = function() { return browser.getTitle(); };

  this.introSection = _getQAelement( 'intro-section' );

  this.introSectionTitle = this.introSection.element( by.css( 'h1' ) );

  this.introSectionLink = this.introSection.element( by.css( 'a' ) );

  this.infoSection = _getQAelement( 'info-section' );

  this.infoSectionTitles = this.infoSection.all( by.css( 'h2' ) );

  this.infoSectionDescriptions = _getQAelement( 'info-section-desc', true );

  this.infoSectionLinks = this.infoSection.all( by.css( 'a' ) );

  this.openingsSection = _getQAelement( 'openings-section' );

  this.contentSidebar = element( by.css( '.content_sidebar' ) );

}


module.exports = Careers;
