'use strict';

var SubPage = require( '../../page_objects/page_sub-pages.js' );

describe( "The Office of Civil Rights' " +
          'Reasonable Accomodation Request Policy Sub-Page', function() {
  var page;

  beforeEach( function() {
    page = new SubPage();
    page.get( 'ReasonableAccommodationRequestPolicy' );
  } );

  it( 'should properly load in a browser', function() {
    expect( page.pageTitle() ).toBe( 'Reasonable Accommodation Request Policy' );
  } );

  it( 'should include page content', function() {
    expect( page.pageContent.getText() ).toContain(
      'ensure equal access and employment opportunities'
    );
  } );

  it( 'should include related links', function() {
    expect( page.relatedLink.isPresent() ).toBe( true );
  } );

  it( 'should NOT include a form', function() {
    expect( page.contentForm.isPresent() ).toBe( false );
  } );

  it( 'should include content markup', function() {
    expect( page.contentMarkup.isPresent() ).toBe( true );
  } );

  it( 'should NOT have subpages', function() {
    expect( page.subpages.isPresent() ).toBe( false );
  } );

  it( 'should NOT have related FAQ', function() {
    expect( page.relatedFAQ.isPresent() ).toBe( false );
  } );

  it( 'should NOT have tags', function() {
    expect( page.contentTags.isPresent() ).toBe( false );
  } );

  it( 'should have office contacts', function() {
    expect( page.officeContact.isPresent() ).toBe( true );
    expect( page.officeContactEmail.getText() )
      .toBe( 'CFPB_EEO@consumerfinance.gov' );
    expect( page.officeContactEmail.getAttribute( 'href' ) )
      .toBe( 'mailto:CFPB_EEO@consumerfinance.gov' );
  } );
} );
