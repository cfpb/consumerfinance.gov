'use strict';

var _getQAElement = require( '../util/qa-element' ).get;

function LandingPage() {

  this.get = function() {
    var baseUrl = '/landing-page/';
    browser.get( baseUrl );
  };

  this.pageTitle = function() { return browser.getTitle(); };

}

function SubLandingPage() {

  this.get = function() {
    var baseUrl = '/sublanding-page/';
    browser.get( baseUrl );
  };

  this.pageTitle = function() { return browser.getTitle(); };

}

function BrowsePage() {

  this.get = function() {
    var baseUrl = '/browse-page/';
    browser.get( baseUrl );
  };

  this.pageTitle = function() { return browser.getTitle(); };

}

function BrowseFilterablePage() {

  this.get = function() {
    var baseUrl = '/browse-filterable-page/';
    browser.get( baseUrl );
  };

  this.pageTitle = function() { return browser.getTitle(); };

}

function SublandingFilterablePage() {

  this.get = function() {
    var baseUrl = '/sublanding-filterable-page/';
    browser.get( baseUrl );
  };

  this.pageTitle = function() { return browser.getTitle(); };

}

function EventArchivePage() {

  this.get = function() {
    var baseUrl = '/event-archive-page/';
    browser.get( baseUrl );
  };

  this.pageTitle = function() { return browser.getTitle(); };

}

function DocumentDetailPage() {

  this.get = function() {
    var baseUrl = '/browse-filterable-page/document-detail';
    browser.get( baseUrl );
  };

  this.pageTitle = function() { return browser.getTitle(); };

}

function LearnPage() {

  this.get = function() {
    var baseUrl = '/browse-filterable-page/learn';
    browser.get( baseUrl );
  };

  this.pageTitle = function() { return browser.getTitle(); };

}

function EventPage() {

  this.get = function() {
    var baseUrl = '/browse-filterable-page/event';
    browser.get( baseUrl );
  };

  this.pageTitle = function() { return browser.getTitle(); };

}

module.exports.landing = LandingPage;
module.exports.sublanding = SubLandingPage;
module.exports.browse = BrowsePage;
module.exports.browse_filterable = BrowseFilterablePage;
module.exports.sublanding_filterable = SublandingFilterablePage;
module.exports.event_archive = EventArchivePage;
module.exports.docdetail = DocumentDetailPage;
module.exports.learn = LearnPage;
module.exports.event = EventPage;
