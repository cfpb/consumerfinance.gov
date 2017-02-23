'use strict';

var _getQAelement = require( '../util/qa-element' ).get;
var relatedLinksSection = require( '../shared_objects/related-links-section' );
var videoPlayer = require( '../shared_objects/video-player' );


function ApplicationProcess() {

  Object.assign( this, relatedLinksSection, videoPlayer );

  this.get = function() {
    browser.get( '/about-us/careers/application-process/' );
  };

  this.pageTitle = function() { return browser.getTitle(); };

  this.sideNav = element( by.css( '.o-secondary-navigation' ) );

  this.introSection = _getQAelement( 'intro-section' );

  this.jobApplicationsInterfaces =
  element.all( by.css( '.job-applications-interfaces .media' ) );

  this.ethicsLink = element( by.css( 'a[href="mailto:EthicsHelp@cfpb.gov"' ) );

  this.infoSection = _getQAelement( 'info-section' );

  this.infoSectionTitles = this.infoSection.all( by.css( 'h2' ) );

  this.infoSectionDescriptions = _getQAelement( 'info-section-desc', true );

  this.infoSectionLinks = this.infoSection.all( by.css( 'a' ) );

}


module.exports = ApplicationProcess;
