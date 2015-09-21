'use strict';

var _getQAElement = require( '../util/QAelement' ).get;

function PastAwards() {

  this.get = function() {
    browser.get( 'doing-business-with-us/past-awards/' );
  };

  this.pageTitle = function() { return browser.getTitle(); };

  this.sideNav = element( by.css( '.nav-secondary' ) );

  this.breadcrumb = element( by.css( '.breadcrumbs_link' ) );

  this.mainTitle = _getQAElement( 'main-title' );

  this.mainSummary = _getQAElement( 'main-summary' );

  this.summaryNavLink = this.mainSummary.element( by.css( 'a' ) );

  this.businessContentTitles =
  element.all( by.css( '.business_page-content h3' ) );

  this.businessContentLinks =
  element.all( by.css( '.business_page-content a' ) );

  this.moreInfoSection = _getQAElement( 'more-info', true );

  this.moreInfoSectionTitles = this.moreInfoSection.all( by.css( 'h2' ) );

  this.moreInfoSectionDescriptions =
  this.moreInfoSection.all( by.css( '.short-desc' ) );

  this.moreInfoSectionLinks = this.moreInfoSection.all( by.css( 'a' ) );

}

module.exports = PastAwards;
