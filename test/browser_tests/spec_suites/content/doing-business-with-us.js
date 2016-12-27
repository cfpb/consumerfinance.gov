'use strict';

var DoingBusinessWithUs =
require( '../../page_objects/page_doing-business-with-us.js' );

var Urlmatcher = require( '../../util/url-matcher' );

describe( 'The Doing Business with Us Page', function() {
  var page;

  beforeAll( function() {
    page = new DoingBusinessWithUs();
    page.get();

    jasmine.addMatchers( Urlmatcher );
  } );


  it( 'should properly load in a browser', function() {
    expect( page.pageTitle() ).toContain( 'Doing business with us' );
  } );

  it( 'should have a side nav', function() {
    expect( page.sideNav.isPresent() ).toBe( true );
  } );

  it( 'should have a main summary', function() {
    expect( page.mainSummary.isPresent() ).toBe( true );
  } );

  it( 'should have a contact link with main summary', function() {
    expect( page.mainSummaryContactLink.getAttribute( 'href' ) )
    .toBe( 'mailto:CFPB_procurement@consumerfinance.gov' );
  } );

  it( 'should have a Business Opportunity section', function() {
    expect( page.businessOpportunitySectionTitle.getText() )
    .toBe( 'Opportunities to work with us' );
  } );

  it( 'should have three Business Opportunity steps', function() {
    var businessStepTitles = [
      'STEP ONE\nRegister with System of Award Management (SAM)',
      'STEP TWO\nIdentify a specific opportunity',
      'STEP THREE\nMonitor upcoming procurement needs'
    ];
    var businessStepLinks = [
      'https://www.sam.gov/',
      'https://www.fbo.gov/?s=agency&mode=form&tab=notices&' +
      'id=e4a0c57cfb98ca60165469a7f9a778a0',
      '/about-us/doing-business-with-us/upcoming-procurement-needs/'
    ];

    expect( page.businessStepTitles.getText() )
    .toEqual( businessStepTitles );
    expect( page.businessStepDescriptions.count() ).toEqual( 3 );
    expect( page.businessStepLinks.getAttribute( 'href' ) )
    .toEqualUrl( businessStepLinks );
  } );

  it( 'should have two More Info sections', function() {
    var moreInfoSectionTitles = [
      'Existing and past service contracts',
      'Small, women-owned, and minority-owned businesses'
    ];
    var moreInfoSectionLinks = [
      '/about-us/doing-business-with-us/past-awards/',
      '/about-us/doing-business-with-us/small-businesses/'
    ];

    expect( page.moreInfoSectionTitles.getText() )
    .toEqual( moreInfoSectionTitles );
    expect( page.moreInfoSectionDescriptions.count() ).toEqual( 2 );
    expect( page.moreInfoSectionLinks.getAttribute( 'href' ) )
    .toEqualUrl( moreInfoSectionLinks );
  } );

} );
