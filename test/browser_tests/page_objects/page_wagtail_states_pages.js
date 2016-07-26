'use strict';

var envvars = require( '../../../config/environment' ).envvars;

function SharedPage() {

  this.get = function() {
    var baseUrl = '/shared-page/';
    browser.get( baseUrl );
  };

  this.getStaging = function() {
    var baseUrl = envvars.DJANGO_STAGING_HOSTNAME + ':' +
                  envvars.TEST_HTTP_PORT + '/shared-page/';
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
    var baseUrl = envvars.DJANGO_STAGING_HOSTNAME + ':' +
                  envvars.TEST_HTTP_PORT + '/shared-draft-page/';
    browser.get( baseUrl );
  };

  this.pageTitle = function() { return browser.getTitle(); };

}

module.exports = {
  sharedpage:    SharedPage,
  shareddraftpage:    SharedDraftPage
};
