'use strict';

var SmallBusinessess =
require( '../../page_objects/page_dbwu-small-businesses.js' );

var Urlmatcher = require( '../../util/url-matcher' );

describe( 'The Small Businesses Page', function() {
  var page;

  beforeAll( function() {
    page = new SmallBusinessess();
    page.get();

    jasmine.addMatchers( Urlmatcher );
  } );

  it( 'should properly load in a browser', function() {
    expect( page.pageTitle() )
    .toContain( 'Doing Business with Us: Small, women-owned,' +
    ' and minority-owned businesses' );
  } );

  it( 'should have a side nav', function() {
    expect( page.sideNav.isPresent() ).toBe( true );
  } );

  it( 'should have a breadcrumb', function() {
    expect( page.breadcrumb.getText() ).toBe( 'Doing Business with Us' );
  } );

  it( 'should have a main summary', function() {
    expect( page.mainSummary.isPresent() ).toBe( true );
  } );

  it( 'should have a summary navigation link', function() {
    expect( page.summaryNavLink.getAttribute( 'href' ) )
    .toBe( browser.baseUrl + '/budget/' );
  } );

  it( 'should have an Awards table', function() {
    expect( page.awardsTable.isPresent() )
    .toBe( true );
  } );

  xit( 'should have Small Business Info sections', function() {
    var BASE_URL = 'http://files.consumerfinance.gov/f/';
    var smallBusinessLinks = [
      BASE_URL + '201305_cfpb_Small-business-guide.pdf',
      BASE_URL + '201310_cfpb_sb-intake-form.pdf',
      BASE_URL + '201310_cfpb_omwi_opportunities_trifold_final.pdf',
      'https://www.sam.gov/'
    ];

    expect( page.smallBusinessDescriptions.count() ).toEqual( 2 );
    expect( page.smallBusinessLinks.getAttribute( 'href' ) )
    .toEqual( smallBusinessLinks );
  } );

  it( 'should have two More Info sections', function() {
    var moreInfoSectionTitles = [
      'How to do business with us',
      'Expected procurement requests'
    ];
    var moreInfoSectionLinks = [
      'https://www.sam.gov/',
      '/about-us/doing-business-with-us/upcoming-procurement-needs/'
    ];

    expect( page.moreInfoSectionTitles.getText() )
    .toEqual( moreInfoSectionTitles );
    expect( page.moreInfoSectionDescriptions.count() ).toEqual( 2 );
    expect( page.moreInfoSectionLinks.getAttribute( 'href' ) )
    .toEqualUrl( moreInfoSectionLinks );
  } );

} );
