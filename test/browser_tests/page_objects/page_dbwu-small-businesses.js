'use strict';

var _getQAElement = require( '../util/qa-element' ).get;

function SmallBusinessess() {

  this.get = function() {
    browser.get( 'doing-business-with-us/small-businesses/' );
  };

  this.pageTitle = function() { return browser.getTitle(); };

  this.sideNav = element( by.css( '.o-secondary-navigation' ) );

  this.breadcrumb = element( by.css( '.breadcrumbs_link' ) );

  this.mainTitle = _getQAElement( 'main-title' );

  this.mainSummary = _getQAElement( 'main-summary' );

  this.summaryNavLink = this.mainSummary.element( by.css( 'a' ) );

  this.smallBusinessInfo = _getQAElement( 'small-business-info', true );

  this.smallBusinessDescriptions = _getQAElement( 'small-business-desc', true );

  this.smallBusinessLinks = this.smallBusinessInfo.all( by.css( 'a' ) );

  this.awardsTable = element( by.css( '.content_main .simple-table' ) );

  this.moreInfoSection = _getQAElement( 'more-info', true );

  this.moreInfoSectionTitles = this.moreInfoSection.all( by.css( 'h2' ) );

  this.moreInfoSectionDescriptions = _getQAElement( 'more-info-desc', true );

  this.moreInfoSectionLinks = this.moreInfoSection.all( by.css( 'a' ) );

}

module.exports = SmallBusinessess;
