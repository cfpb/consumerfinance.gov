'use strict';

var _getQAElement = require( '../util/qa-element' ).get;

function TheBureauHistoryPage() {

  this.get = function( ) {
    browser.get( '/the-bureau/history/' );
  };

  this.pageTitle = function() { return browser.getTitle(); };

  this.sideNav = element( by.css( '.o-secondary-navigation' ) );

  this.intro = _getQAElement( 'history-intro' );

  this.introTitle = _getQAElement( 'history-title' );

  this.introSummary = _getQAElement( 'history-summary' );

  this.socialMediaShare = this.intro.element( by.css( '.m-social-media' ) );

  this.historySections = _getQAElement( 'history-section', true );

  this.historySectionExpandables =
  element.all( by.css( '.history-section-expandable' ) );
}

module.exports = TheBureauHistoryPage;
