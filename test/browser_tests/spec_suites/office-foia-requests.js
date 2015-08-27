'use strict';

var Office = require( '../page_objects/page_office.js' );

describe( 'The Office of FOIA Requests Page', function() {
  var page;

  beforeAll( function() {
    page = new Office();
    page.get( 'FOIARequests' );
  } );

  it( 'should properly load in a browser', function() {
    expect( page.pageTitle() ).toBe( 'FOIA Requests' );
  } );

  it( 'should include main title', function() {
    expect( page.mainTitle.getText() ).toBe( 'FOIA Requests' );
  } );

  it( 'should include intro text', function() {
    expect( page.introText.getText() ).toContain( 'Freedom of Information' );
  } );

  it( 'should NOT include subscription', function() {
    expect( page.subscription.isPresent() ).toBe( false );
  } );

  it( 'should NOT include top story head', function() {
    expect( page.topStoryHead.isPresent() ).toBe( false );
  } );

  it( 'should NOT include top story description', function() {
    expect( page.topStoryDesc.isPresent() ).toBe( false );
  } );

  it( 'should NOT include top story link', function() {
    expect( page.topStoryLink.isPresent() ).toBe( false );
  } );

  it( 'should NOT have resource image', function() {
    expect( page.resourceImg.isPresent() ).toBe( false );
  } );

  it( 'should have resource title', function() {
    expect( page.resourceTitle.getText() ).toBe( 'Expected timeframe' );
  } );

  it( 'should have resource description', function() {
    expect( page.resourceDesc.getText() ).toContain( 'Processing time' );
  } );

  it( 'should NOT have resource link', function() {
    expect( page.resourceLink.isPresent() ).toBe( false );
  } );

  it( 'should have subpages', function() {
    expect( page.subpages.isPresent() ).toBe( true );
  } );

  it( 'should NOT have office content', function() {
    expect( page.officeContent.isPresent() ).toBe( false );
  } );

  it( 'should have tags', function() {
    expect( page.contentTags.isPresent() ).toBe( true );
  } );

  it( 'should have office contacts', function() {
    expect( page.officeContact.isPresent() ).toBe( true );
    expect( page.officeContactEmail.getText() )
      .toBe( 'FOIA@consumerfinance.gov' );
    expect( page.officeContactEmail.getAttribute( 'href' ) )
      .toBe( 'mailto:FOIA@consumerfinance.gov' );
  } );
} );
