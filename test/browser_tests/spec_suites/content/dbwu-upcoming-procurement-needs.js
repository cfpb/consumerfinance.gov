'use strict';

var UpcomingProcurementNeeds =
require( '../../page_objects/page_dbwu-upcoming-procurement-needs.js' );

var Urlmatcher = require( '../../util/url-matcher' );

describe( 'The Upcoming Procurement Needs Page', function() {
  var page;

  beforeAll( function() {
    page = new UpcomingProcurementNeeds();
    page.get();

    jasmine.addMatchers( Urlmatcher );
  } );

  it( 'should properly load in a browser', function() {
    expect( page.pageTitle() )
    .toContain( 'Doing Business with Us: Upcoming Procurement Needs' );
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

  it( 'should have an external Procurement link', function() {
    expect( page.procurementNeedsExternalLink.getAttribute( 'href' ) )
    .toBe( 'https://www.fbo.gov/?s=agency&mode=form&tab=' +
           'notices&id=e4a0c57cfb98ca60165469a7f9a778a0' );
  } );

  it( 'should have an Procurement Needs table', function() {
    expect( page.procurementNeedsTable.isPresent() )
    .toBe( true );
  } );

  it( 'should have two More Info sections', function() {
    var moreInfoSectionTitles = [
      'How to do business with us',
      'Small and disadvantaged businesses'
    ];
    var moreInfoSectionLinks = [
      'https://www.sam.gov/',
      '/about-us/doing-business-with-us/small-businesses/'
    ];

    expect( page.moreInfoSectionTitles.getText() )
    .toEqual( moreInfoSectionTitles );
    expect( page.moreInfoSectionDescriptions.count() ).toEqual( 2 );
    expect( page.moreInfoSectionLinks.getAttribute( 'href' ) )
    .toEqualUrl( moreInfoSectionLinks );
  } );

} );
