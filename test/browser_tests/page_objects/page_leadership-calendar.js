'use strict';

function TheLeadershipCalendarPage() {

  this.get = function( ) {
    browser.get( '/the-bureau/leadership-calendar/' );
  };

  this.pageTitle = function() { return browser.getTitle(); };

  this.sideNav = element( by.css( '.o-secondary-navigation' ) );

  this.intro =
  element( by.css( '[data-qa-hook="leadership-calendar-intro"]' ) );

  this.introSummary =
  this.intro.element(
    by.css( '[data-qa-hook="leadership-calendar-summary"]' )
  );

  this.searchFilter =
  element.all( by.css( '[data-qa-hook="filter"]' ) ).get( 0 );

  this.searchFilterBtn =
  this.searchFilter.all( by.css( '.m-expandable_target' ) ).first();

  this.downloadFilter =
  element.all( by.css( '[data-qa-hook="filter"]' ) ).get( 1 );

  this.downloadFilterBtn =
  this.downloadFilter.all( by.css( '.m-expandable_target' ) ).first();

  this.searchFilterResults =
  element.all( by.css( '[data-qa-hook="leadership-calendar-filter"] tbody' ) );

  this.paginationForm = element( by.css( '.pagination_form' ) );

}

module.exports = TheLeadershipCalendarPage;
