'use strict';

function SubPage() {
  this.get = function( page ) {
    var baseUrl = '/sub-pages/';
    var examplePages = {
        SubmitAnAccommodationRequest:
          baseUrl + 'submit-an-accommodation-request/',
        SocialMediaAccessibility: baseUrl + 'social-media-accessibility/',
        FileAFormalAccessibilityComplaintOrWebsiteFeedback:
          baseUrl + 'file-a-formal-accessibility-complaint-or-website-feedback/'
    };

    browser.get( examplePages[page] );
  };

  this.pageTitle = function() { return browser.getTitle(); };

  this.pageContent = element( by.css( '.sub-page_content' ) );

  this.relatedLink = element( by.css( '.qa-related-links li' ) );

  this.contentForm = element( by.css( '.qa-body-content form' ) );

  this.contentMarkup = element( by.css( '.sub-page_content-markup' ) );

  this.subpages = element( by.css( '.qa-subpage h2' ) );

  this.relatedFAQ = element( by.css( '.qa-related-faq' ) );

  this.contentTags = element( by.css( '.qa-tags' ) );

  this.officeContact = element( by.css( '.office_contact' ) );

  this.officeContactEmail = element( by.css( '.office_contact a[href^="mailto:"]' ) );
}

module.exports = SubPage;
