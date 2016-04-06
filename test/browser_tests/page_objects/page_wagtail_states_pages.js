'use strict';

function DraftPage() {

  this.get = function() {
    var baseUrl = '/draft-page/';
    browser.get( baseUrl );
  };

  this.pageTitle = function() { return browser.getTitle(); };

}

function SharedPage() {

  this.get = function() {
    var baseUrl = '/shared-page/';
    browser.get( baseUrl );
  };

  this.getStaging = function() {
    var baseUrl = 'content.' + process.env.HTTP_HOST + ':' + process.env.HTTP_PORT + '/shared-page/';
    browser.get( baseUrl );
  };

  this.pageTitle = function() { return browser.getTitle(); };

}

function SharedDraftPage() {

  this.get = function() {
    var baseUrl = '/shared-draft-page/';
    browser.get( baseUrl );
  };

  this.pageTitle = function() { return browser.getTitle(); };

}

function LivePage() {

  this.get = function() {
    var baseUrl = '/live-page/';
    browser.get( baseUrl );
  };

  this.pageTitle = function() { return browser.getTitle(); };

}

function LiveDraftPage() {

  this.get = function() {
    var baseUrl = '/live-draft-page/';
    browser.get( baseUrl );
  };

  this.pageTitle = function() { return browser.getTitle(); };

}

module.exports = {
  draftpage: DraftPage,
  sharedpage: SharedPage,
  livepage: LivePage,
  livedraftpage: LiveDraftPage,
};
