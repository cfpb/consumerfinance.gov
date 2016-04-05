'use strict';

var _getQAElement = require( '../util/qa-element' ).get;

function PastAwards() {

  this.get = function() {
    browser.get( '/about-us/doing-business-with-us/past-awards/' );
  };

  this.pageTitle = function() { return browser.getTitle(); };

  this.sideNav = element( by.css( '.o-secondary-navigation' ) );

  this.breadcrumb = element( by.css( '.breadcrumbs_link' ) );

  this.mainSummary = _getQAElement( 'main-summary' );

  this.businessContentTitles =
  element.all( by.css( '.business_page-content h3' ) );

  this.businessContentLinks =
  element.all( by.css( '.business_page-content a' ) );

  this.moreInfoSection = _getQAElement( 'more-info', true );

  this.moreInfoSectionTitles = this.moreInfoSection.all( by.css( 'h2' ) );

  this.moreInfoSectionDescriptions = _getQAElement( 'more-info-desc', true );

  this.moreInfoSectionLinks = this.moreInfoSection.all( by.css( 'a' ) );

}

module.exports = PastAwards;
