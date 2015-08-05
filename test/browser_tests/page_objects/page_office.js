'use strict';

function OfficePage() {
  this.get = function( page ) {
    var baseUrl = '/offices/';
    var examplePages = {
        Accessibility:            baseUrl + 'accessibility/',
        CFPBOmbudsman:            baseUrl + 'cfpb-ombudsman/',
        FOIARequests:             baseUrl + 'foia-requests/',
        OfficeOfCivilRights:      baseUrl + 'office-of-civil-rights/',
        OpenGovernment:           baseUrl + 'open-government/',
        PaymentsToHarmedConsumer: baseUrl + 'payments-to-harmed-consumers/',
        PlainWriting:             baseUrl + 'plain-writing/',
        Privacy:                  baseUrl + 'privacy/',
        ProjectCatalyst:          baseUrl + 'project-catalyst/'
    };

    browser.get( examplePages[page] );
  };

  this.pageTitle = function() { return browser.getTitle(); };

  this.mainTitle = element( by.css( '.qa-main-title' ) );

  this.introText = element( by.css( '.office_intro-text' ) );

  this.subscription = element( by.css( '.qa-subscription' ) );

  this.topStoryHead = element( by.css( '.qa-top-story-head' ) );

  this.topStoryDesc = element( by.css( '.qa-top-story-desc' ) );

  this.topStoryLink = element( by.css( '.qa-top-story-link' ) );

  this.resourceImg = element( by.css( '.qa-resource-img' ) );

  this.resourceTitle = element( by.css( '.qa-resource-title' ) );

  this.resourceDesc = element( by.css( '.qa-resource-desc' ) );

  this.resourceLink = element( by.css( '.qa-resource-link' ) );

  this.subpages = element( by.css( '.qa-subpage h2' ) );

  this.officeContent = element( by.css( '.qa-office-content h2' ) );

  this.contentTags = element( by.css( '.qa-tags' ) );

  this.officeContact = element( by.css( '.office_contact' ) );

  this.officeContactEmail = element( by.css( '.office_contact a[href^="mailto:"]' ) );
}

module.exports = OfficePage;
