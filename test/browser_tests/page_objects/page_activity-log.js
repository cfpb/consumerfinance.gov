'use strict';

var filter = require( '../shared_objects/filter.js' );
var filterableListControl =
  require( '../shared_objects/filterable-list-control.js' );
var pagination = require( '../shared_objects/pagination' );

function ActivityLog() {
  Object.assign( this, filter, filterableListControl, pagination );

  this.get = function() {
    browser.get( '/activity-log/' );
  };

  this.pageTitle = function() { return browser.getTitle(); };

  this.mainTitle = element( by.css( '[data-qa-hook="main-title"]' ) );

  this.mainSummary = element( by.css( '[data-qa-hook="main-summary"]' ) );
}

module.exports = ActivityLog;
