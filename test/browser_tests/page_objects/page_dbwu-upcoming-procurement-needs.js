'use strict';

var _getQAElement = require( '../util/qa-element' ).get;

function UpcomingProcurementNeeds() {

  this.get = function() {
    var url = '/about-us/doing-business-with-us/upcoming-procurement-needs/';
    browser.get( url );
  };

  this.pageTitle = function() { return browser.getTitle(); };

  this.sideNav = element( by.css( '.o-secondary-navigation' ) );

  this.mainSummary = _getQAElement( 'main-summary' );

  this.breadcrumb = element( by.css( '.breadcrumbs_link' ) );

  this.procurementNeedsExternalLink =
  element( by.css( '[data-qa-hook="main-summary"] + p a' ) );

  this.procurementNeedsTable =
  element( by.css( '.content_main table' ) );

  this.moreInfoSection = _getQAElement( 'more-info', true );

  this.moreInfoSectionTitles = this.moreInfoSection.all( by.css( 'h2' ) );

  this.moreInfoSectionDescriptions = _getQAElement( 'more-info-desc', true );

  this.moreInfoSectionLinks = this.moreInfoSection.all( by.css( 'a' ) );

}

module.exports = UpcomingProcurementNeeds;
