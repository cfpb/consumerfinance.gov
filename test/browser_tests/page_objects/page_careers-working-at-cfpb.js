'use strict';

var _getQAelement = require( '../util/QAelement' ).get;
var careersSocialSection =
require( '../shared_objects/careers-social-section' );
var relatedLinksSection = require( '../shared_objects/related-links-section' );


function WorkingAtCFPB() {

  Object.assign( this, careersSocialSection, relatedLinksSection );

  this.get = function() {
    browser.get( '/careers/working-at-cfpb/' );
  };

  this.pageTitle = function() { return browser.getTitle(); };

  this.sideNav = element( by.css( '.nav-secondary' ) );

  this.introSection = _getQAelement( 'intro-section' );

  this.introSectionTitle = this.introSection.element( by.css( 'h1' ) );

  this.introSectionLink = this.introSection.element( by.css( 'a' ) );

  this.mobileCarouselItems =
  element.all( by.css( '.media-stack_item' ) );

  this.infoSection = _getQAelement( 'info-section' );

  this.infoSectionTitles = this.infoSection.all( by.css( 'h2' ) );

  this.infoSectionDescriptions =
  this.infoSection.all( by.css( '.short-desc' ) );

  this.infoSectionLinks = this.infoSection.all( by.css( 'a' ) );

}


module.exports = WorkingAtCFPB;
