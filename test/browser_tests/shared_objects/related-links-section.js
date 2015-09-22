'use strict';

var _relatedLinksSection = element( by.css( '.related-links' ) );

var relatedLinksSection = {

  relatedLinksSection: _relatedLinksSection,

  relatedLinksSectionTitles: _relatedLinksSection.all( by.css( 'h2' ) ),

  relatedLinksSectionDescriptions:
  _relatedLinksSection.all( by.css( '.short-desc' ) ),

  relatedLinks: _relatedLinksSection.all( by.css( 'a' ) )
};

module.exports = relatedLinksSection;
