'use strict';

function BudgetStrategicPlan() {

  this.get = function() {
    browser.get( 'budget/strategic-plan/' );
  };

  this.pageTitle = function() { return browser.getTitle(); };

  this.sideNav = element( by.css( '.o-secondary-navigation' ) );

  this.breadcrumb = element( by.css( '.breadcrumbs_link' ) );

  this.mainTitle = element( by.css( '.content_main h1' ) );

  this.mainSummary = element( by.css( '.content_main p.h3' ) );

  this.mainSubTitle = element( by.css( '.content_main h2' ) );

  this.mainLinks = element.all( by.css( '.content_main a' ) );

}

module.exports = BudgetStrategicPlan;
