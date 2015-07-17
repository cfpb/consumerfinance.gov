'use strict';

function ContactUsPage() {
  this.get = function() {
    browser.get( '/contact-us/' );
  };

  this.pageTitle = function() { return browser.getTitle(); };
  this.complaintPhone = element.all( by.partialLinkText( '(2372)' ) );
  this.giEmail = element( by.partialLinkText( 'info@consumerfinance.gov' ) );
  this.giPhone = element( by.partialLinkText( '(202) 435-7000' ) );
  this.offices = element.all( by.css( '.contact-list article' ) );
  this.firstOfficeLabel = this.offices.first().element(
    by.css( '.expandable_label' )
  );
  this.lastOfficeLabel = this.offices.last().element(
    by.css( '.expandable_label' )
  );
}

module.exports = ContactUsPage;
