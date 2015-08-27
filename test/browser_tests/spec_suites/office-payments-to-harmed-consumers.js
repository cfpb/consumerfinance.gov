'use strict';

var Office = require( '../page_objects/page_office.js' );

describe( 'The Payments to Harmed Consumers Office Page', function() {
  var page;

  beforeAll( function() {
    page = new Office();
    page.get( 'PaymentsToHarmedConsumer' );
  } );

  it( 'should properly load in a browser', function() {
    expect( page.pageTitle() ).toBe( 'Payments to Harmed Consumers' );
  } );

  it( 'should include main title', function() {
    expect( page.mainTitle.getText() ).toBe( 'Payments to Harmed Consumers' );
  } );

  it( 'should include intro text', function() {
    expect( page.introText.getText() ).toContain( 'Congress has authorized' );
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

  it( 'should NOT have resource title', function() {
    expect( page.resourceTitle.isPresent() ).toBe( false );
  } );

  it( 'should NOT have resource description', function() {
    expect( page.resourceDesc.isPresent() ).toBe( false );
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

  it( 'should NOT have office contacts', function() {
    expect( page.officeContact.isPresent() ).toBe( false );
  } );
} );
