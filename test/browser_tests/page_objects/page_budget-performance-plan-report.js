'use strict';

function BudgetPerformancePlanReport() {

  this.get = function() {
    browser.get( 'budget/performance-plan-report/' );
  };

  this.pageTitle = function() { return browser.getTitle(); };

  this.sideNav = element( by.css( '.o-secondary-navigation' ) );

  this.breadcrumb = element( by.css( '.breadcrumbs_link' ) );

  this.mainTitle = element( by.css( '.content_main h1' ) );

  this.mainSummary = element( by.css( '.content_main p.h3' ) );

  this.performancePlanTitles = element.all( by.css( '.performance-plan h4' ) );

  this.performancePlanLinks = element.all( by.css( '.performance-plan a' ) );

}

module.exports = BudgetPerformancePlanReport;
