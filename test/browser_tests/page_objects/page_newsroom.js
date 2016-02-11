'use strict';

var filter = require( '../shared_objects/filter.js' );
var pagination = require( '../shared_objects/pagination' );
var stayInformedSection = require( '../shared_objects/stay-informed-section' );
var rssSection = require( '../shared_objects/rss-section' );

var _getQAElement = require( '../util/QAelement' ).get;

function Newsroom() {

  Object.assign( this, filter, pagination, stayInformedSection, rssSection );

  this.get = function() {
    browser.get( '/newsroom/' );
  };

  this.pageTitle = browser.getTitle;

  this.mainTitle = _getQAElement( 'main-title' );

  this.sideNav = element( by.css( '.nav-secondary' ) );

  this.featuredTopic = element( by.css( '.featured-topic' ) );

  this.featuredTopicTitle =
  this.featuredTopic.element( by.css( '.summary_header' ) );

  this.featuredTopicSummaryText =
  this.featuredTopic.all( by.css( '.summary_cols' ) ).get( 0 );

  this.featuredTopicSummaryLinks =
  this.featuredTopic.all( by.css( '.summary_cols' ) ).get( 1 );

  this.relatedContent = element( by.css( '.related_content' ) );

  this.relatedLinks =
  this.relatedContent.element( by.css( '.related_content' ) );

  this.upcomingEvents =
  this.relatedContent.element( by.css( '.upcoming-events' ) );

}

module.exports = Newsroom;
