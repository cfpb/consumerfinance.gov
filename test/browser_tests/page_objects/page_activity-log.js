'use strict';

function ActivityLog() {
  this.get = function() {
    browser.get( '/activity-log/' );
  };

  this.pageTitle = function() { return browser.getTitle(); };

  this.mainTitle = element( by.css( '[data-qa-hook="main-title"]' ) );

  this.mainSummary = element( by.css( '[data-qa-hook="main-summary"]' ) );

  this.searchFilter = element( by.css(  '[data-qa-hook="filter"]' ) );

  this.searchFilterBtn =
  this.searchFilter.element( by.css( '.m-expandable_target' ) );

  this.searchFilterShowBtn =
  this.searchFilter.element( by.css( '.m-expandable_cue-open' ) );

  this.searchFilterHideBtn =
  this.searchFilter.element( by.css( '.m-expandable_cue-close' ) );

  this.searchFilterResults =
  element.all( by.css( '[data-qa-hook="filter-results"] tr' ) );

  this.paginationForm = element( by.css( '.pagination_form' ) );

  this.paginationPrevBtn = element( by.css( '.pagination_prev' ) );

  this.paginationNextBtn = element( by.css( '.pagination_next' ) );

  this.paginationPageInput = element( by.css( '.pagination_current-page' ) );
}

module.exports = ActivityLog;
