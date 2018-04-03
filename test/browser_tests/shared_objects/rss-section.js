const _getQAelement = require( '../util/qa-element' ).get;

const _rssSubscribeSection = _getQAelement( 'rss-subscribe-section' );

const rssSubscribeSection = {
  rssSubscribeSection: _rssSubscribeSection,

  rssSubscribeDescription: _getQAelement( 'rss-subscribe-desc' ),

  rssSubscribeBtn: _rssSubscribeSection.element( by.css( '.btn' ) )

};

module.exports = rssSubscribeSection;
