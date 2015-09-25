'use strict';

var _getQAelement = require( '../util/QAelement' ).get;
var _socialSection = _getQAelement( 'social-section' );

var careersSocialSection = {

  socialSection: _socialSection,

  socialSectionTitles: _socialSection.all( by.css( 'h2' ) ),

  socialSectionDescriptions: _socialSection.all( by.css( '.short-desc' ) ),

  socialSectionLinks: _socialSection.all( by.css( 'a' ) )
};

module.exports = careersSocialSection;
