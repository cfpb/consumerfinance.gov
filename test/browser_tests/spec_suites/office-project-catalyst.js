'use strict';

var Office = require( '../page_objects/page_office.js' );

describe( 'The Project Catalyst Page', function() {
  var page;

  beforeAll( function() {
    page = new Office();
    page.get( 'ProjectCatalyst' );
  } );

  it( 'should properly load in a browser', function() {
    expect( page.pageTitle() ).toBe( 'Project Catalyst' );
  } );

  it( 'should include main title', function() {
    expect( page.mainTitle.getText() ).toBe( 'Project Catalyst' );
  } );

  it( 'should include intro text', function() {
    expect( page.introText.getText() ).toContain( 'Our mission' );
  } );

  it( 'should NOT include subscription', function() {
    expect( page.subscription.isPresent() ).toBe( false );
  } );

  it( 'should include top story head', function() {
    expect( page.topStoryHead.getText() ).toBe( 'Talk to Us' );
  } );

  it( 'should include top story description', function() {
    expect( page.topStoryDesc.getText() ).toContain( 'We have a lot to talk' );
  } );

  it( 'should include top story link', function() {
    expect( page.topStoryLink.getText() ).toContain( 'Email us at' );
    expect( page.topStoryLink.getAttribute( 'href' ) )
      .toBe( 'mailto:ProjectCatalyst@cfpb.gov' +
             '?subject=I%27ve%20got%20an%20idea...' );
  } );

  it( 'should NOT have resource image', function() {
    expect( page.resourceImg.isPresent() ).toBe( false );
  } );

  it( 'should have resource title', function() {
    expect( page.resourceTitle.isPresent() ).toBe( true );
  } );

  it( 'should have resource description', function() {
    expect( page.resourceDesc.isPresent() ).toBe( true );
  } );

  it( 'should have resource link', function() {
    expect( page.resourceLink.isPresent() ).toBe( true );
  } );

  it( 'should NOT have subpages', function() {
    expect( page.subpages.isPresent() ).toBe( true );
  } );

  it( 'should have office content', function() {
    expect( page.officeContent.getText() )
      .toBe( 'How we’ll handle your information' );
  } );

  it( 'should have tags', function() {
    expect( page.contentTags.isPresent() ).toBe( true );
  } );

  it( 'should have office contacts', function() {
    expect( page.officeContact.isPresent() ).toBe( true );
    expect( page.officeContactEmail.getText() )
      .toBe( 'CFPB_ProjectCatalyst@consumerfinance.gov' );
    expect( page.officeContactEmail.getAttribute( 'href' ) )
      .toBe( 'mailto:CFPB_ProjectCatalyst@consumerfinance.gov' );
  } );
} );
