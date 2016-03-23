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

  this.directorImage = _getQAElement( 'director-bio-image' );

  this.mediaDownloads = element.all(
  by.css( '[data-qa-hook="director-media-downloads"] .jump-link__download' ) );

  this.bioDownload = this.mediaDownloads.get( 0 );

  this.highResImageDownload = this.mediaDownloads.get( 1 );

  this.lowResImageDownload = this.mediaDownloads.get( 2 );

}

module.exports = TheAboutDirectorPage;
