'use strict';

function SharedPage() {

  this.get = function() {
    var baseUrl = '/shared-page/';
    browser.get( baseUrl );
  };

  this.getStaging = function() {
    var baseUrl = process.env.STAGING_HOSTNAME + ':' +
                  process.env.HTTP_PORT + '/shared-page/';
    browser.get( baseUrl );
  };

  this.pageTitle = function() { return browser.getTitle(); };

}

function SharedDraftPage() {

  this.get = function() {
    var baseUrl = '/shared-draft-page/';
    browser.get( baseUrl );
  };

  this.getStaging = function() {
    var baseUrl = process.env.STAGING_HOSTNAME + ':' +
                  process.env.HTTP_PORT + '/shared-draft-page/';
    browser.get( baseUrl );
  };

  this.pageTitle = function() { return browser.getTitle(); };

}

module.exports = {
  sharedpage:    SharedPage,
  shareddraftpage:    SharedDraftPage
};
