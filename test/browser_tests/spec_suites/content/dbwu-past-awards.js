'use strict';

var PastAwards =
require( '../../page_objects/page_dbwu-past-awards.js' );

var Urlmatcher = require( '../../util/url-matcher' );

describe( 'The Past Awards Page', function() {
  var page;

  beforeAll( function() {
    page = new PastAwards();
    page.get();

    jasmine.addMatchers( Urlmatcher );
  } );

  it( 'should properly load in a browser', function() {
    expect( page.pageTitle() )
    .toContain( 'Doing Business with Us: Past Awards' );
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

  it( 'should have Business content', function() {
    expect( page.businessContentTitles.count() ).toBeGreaterThan( 0 );
    expect( page.businessContentLinks.count() ).toBeGreaterThan( 0 );
    page.businessContentLinks.getAttribute( 'href' )
    .then( function( values ) {
      expect( values.join().indexOf( '.pdf' ) > -1 ).toBe( true );
    } );
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
