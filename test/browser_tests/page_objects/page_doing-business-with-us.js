'use strict';

var _getQAElement = require( '../util/QAelement' ).get;

function DoingBusinessWithUs() {

  this.get = function() {
    browser.get( 'doing-business-with-us/' );
  };

  this.pageTitle = function() { return browser.getTitle(); };

  this.sideNav = element( by.css( '.nav-secondary' ) );

  this.mainTitle = _getQAElement( 'main-title' );

  this.mainSummary = _getQAElement( 'main-summary' );

  this.mainSummaryContactLink = this.mainSummary.element( by.css( 'a' ) );

  this.businessOpportunitySection = _getQAElement( 'business-opportunities' );

  this.businessOpportunitySectionTitle =
  this.businessOpportunitySection.element( by.css( 'h2' ) );

  this.businessSteps =
  this.businessOpportunitySection.all( by.css( '.content-l_col-1-3' ) );

  this.businessStepTitles = this.businessSteps.all( by.css( 'h3' ) );

  this.businessStepDescriptions =
  this.businessSteps.all( by.css( '.short-desc' ) );

  this.businessStepLinks = this.businessSteps.all( by.css( 'a' ) );

  this.moreInfoSection = _getQAElement( 'more-info' );

  this.moreInfoSectionTitles = this.moreInfoSection.all( by.css( 'h2' ) );

  this.moreInfoSectionDescriptions =
  this.moreInfoSection.all( by.css( '.short-desc' ) );

  this.moreInfoSectionLinks = this.moreInfoSection.all( by.css( 'a' ) );

}

module.exports = DoingBusinessWithUs;
