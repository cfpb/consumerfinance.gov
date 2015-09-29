'use strict';

var _assign = require( 'lodash' ).assign;
var _getQAelement = require( '../util/QAelement' ).get;
var careersSocialSection =
require( '../shared_objects/careers-social-section' );
var relatedLinksSection = require( '../shared_objects/related-links-section' );


function CurrentOpenings() {

  _assign( this, careersSocialSection, relatedLinksSection );

  this.get = function() {
    browser.get( '/careers/current-openings/' );
  };

  this.pageTitle = function() { return browser.getTitle(); };

  this.sideNav = element( by.css( '.nav-secondary' ) );

  this.introSection = _getQAelement( 'intro-section' );

  this.introSectionTitle = this.introSection.element( by.css( 'h1' ) );

  this.introSectionLink = this.introSection.element( by.css( 'a' ) );

  this.jobOpeningsTable =
  _getQAelement( 'job-openings-section' ).element( by.css( 'table' ) );

  this.infoSection = _getQAelement( 'info-section' );

  this.infoSectionTitles = this.infoSection.all( by.css( 'h2' ) );

  this.infoSectionDescriptions =
  this.infoSection.all( by.css( '.short-desc' ) );

  this.infoSectionLinks = this.infoSection.all( by.css( 'a' ) );

}


module.exports = CurrentOpenings;
