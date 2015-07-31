'use strict';

function OfficePage() {
  this.get = function( officePage ) {
    var examplePages = {
        CFPBOmbudsman:              '/offices/cfpb-ombudsman/',
        FOIARequests:               '/offices/foia-requests/',
        OpenGovernment:             '/offices/open-government/',
        PaymentsToHarmedConsumer:   '/offices/payments-to-harmed-consumers/',
        PlainWriting:               '/offices/plain-writing/',
        Privacy:                    '/offices/privacy/',
        ProjectCatalyst:            '/offices/project-catalyst/'
    };

    browser.get( examplePages[officePage] );
  };

  this.pageTitle = function() { return browser.getTitle(); };

  this.mainTitle = element( by.css( '.qa-main-title' ) );

  this.introText = element( by.css( '.office_intro-text' ) );

  this.subscription = element( by.css( '.qa-subscription') );

  this.topStoryHead = element( by.css( '.qa-top-story-head' ) );

  this.topStoryDesc = element( by.css( '.qa-top-story-desc' ) );

  this.topStoryLink = element( by.css( '.qa-top-story-link' ) );

  this.resourceImg = element( by.css( '.qa-resource-img' ) );

  this.resourceTitle = element( by.css( '.qa-resource-title' ) );

  this.resourceDesc = element( by.css( '.qa-resource-desc' ) );

  this.resourceLink = element( by.css( '.qa-resource-link' ) );

  this.subpages = element( by.css( '.qa-subpage h2' ) );

  this.officeContent = element( by.css( '.qa-office-content h2' ) );

  this.officeTags = element( by.css( '.qa-office-tags h1' ) );

  this.officeContact = element( by.css( '.office_contact' ) );
}

module.exports = OfficePage;
