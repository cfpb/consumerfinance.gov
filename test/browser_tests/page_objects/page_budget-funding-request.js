'use strict';

function BudgetFundingRequest() {

  this.get = function() {
    browser.get( 'budget/funding-request/' );
  };

  this.pageTitle = function() { return browser.getTitle(); };

  this.sideNav = element( by.css( '.o-secondary-navigation' ) );

  this.breadcrumb = element( by.css( '.breadcrumbs_link' ) );

  this.mainTitle = element( by.css( '.content_main h1' ) );

  this.mainSummary = element( by.css( '.content_main p.h3' ) );

  this.fundingRequestTitles = element.all( by.css( '.funding-request h4' ) );

  this.fundingRequestLinks = element.all( by.css( '.funding-request a' ) );

}

module.exports = BudgetFundingRequest;
