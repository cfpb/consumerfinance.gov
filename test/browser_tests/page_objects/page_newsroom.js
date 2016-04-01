'use strict';

var filter = require( '../shared_objects/filter.js' );
var pagination = require( '../shared_objects/pagination' );
var stayInformedSection = require( '../shared_objects/stay-informed-section' );
var rssSection = require( '../shared_objects/rss-section' );

var _getQAElement = require( '../util/qa-element' ).get;

function Newsroom() {

  Object.assign( this, filter, pagination, stayInformedSection, rssSection );

  this.get = function() {
    browser.get( '/newsroom/' );
  };

  this.pageTitle = browser.getTitle;

  this.mainTitle = _getQAElement( 'main-title' );

  this.sideNav = element( by.css( '.o-secondary-navigation' ) );

  this.relatedContent = element( by.css( '.related_content' ) );

  this.relatedLinks =
  this.relatedContent.element( by.css( '.related_content' ) );

  this.upcomingEvents =
  this.relatedContent.element( by.css( '.upcoming-events' ) );

}

module.exports = Newsroom;
