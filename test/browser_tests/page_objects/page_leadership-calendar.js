'use strict';

function TheLeadershipCalendarPage() {

  this.get = function( ) {
    browser.get( '/the-bureau/leadership-calendar/' );
  };

  this.pageTitle = function() { return browser.getTitle(); };

  this.sideNav = element( by.css( '.o-secondary-navigation' ) );

  this.intro =
  element( by.css( '[data-qa-hook="leadership-calendar-intro"]' ) );

  this.introTitle = this.intro.all( by.css( 'h1' ) ).first();

  this.introSummary =
  this.intro.element(
    by.css( '[data-qa-hook="leadership-calendar-summary"]' )
  );

  this.socialMediaShare = this.intro.element( by.css( '.m-social-media' ) );

  this.searchFilter = element.all( by.css( '.js-post-filter' ) ).get( 0 );

  this.searchFilterBtn =
  this.searchFilter.all( by.css( '.expandable_target' ) ).first();

  this.downloadFilter = element.all( by.css( '.js-post-filter' ) ).get( 1 );

  this.downloadFilterBtn =
  this.downloadFilter.all( by.css( '.expandable_target' ) ).first();

  this.searchFilterResults =
  element.all( by.css( '[data-qa-hook="leadership-calendar-filter"] tbody' ) );

  this.paginationForm = element( by.css( '.pagination_form' ) );

}

module.exports = TheLeadershipCalendarPage;
