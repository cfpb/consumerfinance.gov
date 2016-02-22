'use strict';

var _getQAElement = require( '../util/qa-element' ).get;

function TheAboutDirectorPage() {

  this.get = function( page ) {
    var baseUrl = '/the-bureau/';

    var pageLookup = {
      director:       baseUrl + 'about-director/',
      deputyDirector: baseUrl + 'about-deputy-director/'
    };

    browser.get( pageLookup[page] );
  };

  this.pageTitle = function() { return browser.getTitle(); };

  this.sideNav = element( by.css( '.o-secondary-navigation' ) );

  this.directorBio = _getQAElement( 'director-bio' );

  this.directorBioSummary = _getQAElement( 'director-bio-summary' );

  this.directorCorner = _getQAElement( 'director-corner' );

  this.directorHistory = _getQAElement( 'director-history' );

  this.directorTitle = _getQAElement( 'director-bio-title' );

  this.directorImage = _getQAElement( 'director-bio-image' );

  this.mediaDownloads = element.all(
  by.css( '[data-qa-hook="director-media-downloads"] .jump-link__download' ) );

  this.bioDownload = this.mediaDownloads.get( 0 );

  this.highResImageDownload = this.mediaDownloads.get( 1 );

  this.lowResImageDownload = this.mediaDownloads.get( 2 );

  this.moreInfo = _getQAElement( 'director-more-info' );

  this.moreInfoTitle = this.moreInfo.element( by.css( 'h2' ) );

  this.moreInfoItems = this.moreInfo.all( by.css( '.content-l_col-1-3' ) );

  this.relatedLinks = element( by.css( '.related-links' ) );

  this.socialMediaShare = element( by.css( '.m-social-media' ) );

  this.speakingInfo = _getQAElement( 'director-speaking-info' );

  this.speakingInfoEmail = this.speakingInfo.element( by.css( 'a' ) );

}

module.exports = TheAboutDirectorPage;
