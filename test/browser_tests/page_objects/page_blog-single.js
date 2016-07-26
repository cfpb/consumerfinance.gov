'use strict';

var stayInformedSection = require( '../shared_objects/stay-informed-section' );
var rssSection = require( '../shared_objects/rss-section' );

function BlogSingle() {

  Object.assign( this, stayInformedSection, rssSection );

  this.get = function() {
    browser.get( '/blog/lessons-weve-learned/' );
  };

  this.pageTitle = function() { return browser.getTitle(); };

  this.postTitle = element( by.css( 'header h1' ) );

  this.postByLine = element( by.css( 'header .byline' ) );

  this.postBody = element( by.css( '.post .post_body' ) );

  this.share = element( by.css( 'header .m-social-media__share' ) );

  this.breadcrumbs = element( by.css( '.breadcrumbs' ) );

  this.tags = element( by.css( '.tags' ) );

  this.contentSidebar = element( by.css( '.content_sidebar' ) );

  this.relatedPosts =
    this.contentSidebar.element( by.css( '.related-posts' ) );

  this.relatedPostsTitle =
    this.relatedPosts.element( by.css( '.header-slug_inner' ) );
}

module.exports = BlogSingle;
