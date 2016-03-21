'use strict';

var _getQAElement = require( '../util/qa-element' ).get;

function DoingBusinessWithUs() {

  this.get = function() {
    browser.get( 'doing-business-with-us/' );
  };

  this.pageTitle = function() { return browser.getTitle(); };

  this.sideNav = element( by.css( '.o-secondary-navigation' ) );

  this.mainTitle = _getQAElement( 'main-title' );

  this.mainSummary = _getQAElement( 'main-summary' );

  this.mainSummaryContactLink = this.mainSummary.element( by.css( 'a' ) );

  this.businessOpportunitySection =
  element( by.css( '.block__business-step_container' ) );

  this.businessOpportunitySectionTitle =
  this.businessOpportunitySection.element( by.css( 'h2' ) );

  this.businessSteps =
  this.businessOpportunitySection.all( by.css( '.content-l_col-1-3' ) );

  this.businessStepTitles = this.businessSteps.all( by.css( 'h3' ) );

  this.businessStepDescriptions = _getQAElement( 'business-step-desc', true );

  this.businessStepLinks = this.businessSteps.all( by.css( 'a' ) );

  this.moreInfoSection = _getQAElement( 'more-info', true );

  this.moreInfoSectionTitles = this.moreInfoSection.all( by.css( 'h2' ) );

  this.moreInfoSectionDescriptions = _getQAElement( 'more-info-desc', true );

  this.moreInfoSectionLinks = this.moreInfoSection.all( by.css( 'a' ) );

}

module.exports = DoingBusinessWithUs;
