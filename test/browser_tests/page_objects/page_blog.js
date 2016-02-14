'use strict';

var filter = require( '../shared_objects/filter.js' );
var pagination = require( '../shared_objects/pagination' );
var stayInformedSection = require( '../shared_objects/stay-informed-section' );
var rssSection = require( '../shared_objects/rss-section' );
var _getQAelement = require( '../util/QAelement' ).get;

function Blog() {

  Object.assign( this, filter, pagination, stayInformedSection, rssSection );

  this.get = function() {
    browser.get( '/blog/' );
  };

  this.pageTitle = function() { return browser.getTitle(); };

  this.mainTitle = _getQAelement( 'main-title' );

  this.contentSidebar = element( by.css( '.content_sidebar' ) );

  this.popularStories =
  this.contentSidebar.element( by.css( '.popular-stories' ) );

  this.popularStoriesTitle =
  this.popularStories.element( by.css( '.header-slug_inner' ) );
}

module.exports = Blog;
