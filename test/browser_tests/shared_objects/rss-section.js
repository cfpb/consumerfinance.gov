'use strict';

var _getQAelement = require( '../util/qa-element' ).get;

var _rssSubscribeSection = _getQAelement( 'rss-subscribe-section' );

var rssSubscribeSection = {
  rssSubscribeSection: _rssSubscribeSection,

  rssSubscribeDescription: _getQAelement( 'rss-subscribe-desc' ),

  rssSubscribeBtn:
  _rssSubscribeSection.element( by.css( '.btn' ) )

};

module.exports = rssSubscribeSection;
