'use strict';

var filter = require( '../shared_objects/filter.js' );
var filterableListControl =
require( '../shared_objects/filterable-list-control.js' );
var multiSelect = require( '../shared_objects/multiselect' );
var pagination = require( '../shared_objects/pagination' );
var stayInformedSection = require( '../shared_objects/stay-informed-section' );
var rssSection = require( '../shared_objects/rss-section' );
var _getQAelement = require( '../util/qa-element' ).get;

function Blog() {

  Object.assign( this, filter, filterableListControl, multiSelect,
    pagination, stayInformedSection, rssSection );

  this.get = function() {
    browser.get( '/sfp/' );
  };

  this.pageTitle = function() { return browser.getTitle(); };

  this.mainTitle = _getQAelement( 'main-title' );

  this.contentSidebar = element( by.css( '.content_sidebar' ) );

  this.popularStories =
  this.contentSidebar.element( by.css( '.popular-stories' ) );

  this.popularStoriesTitle =
  this.popularStories.element( by.css( '.header-slug_inner' ) );

  this.results = element( by.css( '.o-post-preview_content' ) );
}

module.exports = Blog;
