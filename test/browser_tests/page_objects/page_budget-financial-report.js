'use strict';

function BudgetFinancialReport() {

  this.get = function() {
    browser.get( 'budget/financial-report/' );
  };

  this.pageTitle = function() { return browser.getTitle(); };

  this.sideNav = element( by.css( '.o-secondary-navigation' ) );

  this.breadcrumb = element( by.css( '.breadcrumbs_link' ) );

  this.mainTitle = element( by.css( '.content_main h1' ) );

  this.mainSummary = element( by.css( '.content_main p.h3' ) );

  this.financialReportTitles = element.all( by.css( '.financial-report h4' ) );

  this.financialReportLinks = element.all( by.css( '.financial-report a' ) );

}

module.exports = BudgetFinancialReport;
