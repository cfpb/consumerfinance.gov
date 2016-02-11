'use strict';

var _getQAelement = require( '../util/QAelement' ).get;

var _rssSubscribeSection = _getQAelement( 'rss-subscribe-section' );

var rssSubscribeSection = {
  rssSubscribeSection: _rssSubscribeSection,

  rssSubscribeDescription:
  _rssSubscribeSection.element( by.css( '.short-desc' ) ),

  rssSubscribeBtn:
  _rssSubscribeSection.element( by.css( '.btn' ) )

};

module.exports = rssSubscribeSection;
