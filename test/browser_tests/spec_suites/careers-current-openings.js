'use strict';

var CurrentOpenings = require(
    '../page_objects/page_careers-current-openings.js'
  );

var Urlmatcher = require( '../util/url-matcher' );

describe( 'The Current Openings Page', function() {
  var page;

  beforeAll( function() {
    page = new CurrentOpenings();
    page.get();

    jasmine.addMatchers( Urlmatcher );
  } );

  it( 'should properly load in a browser', function() {
    expect( page.pageTitle() ).toBe( 'Current Openings' );
  } );

  it( 'should have a sideNav', function() {
    expect( page.sideNav.isPresent() ).toBe( true );
  } );

  it( 'should have an intro title', function() {
    expect( page.introSectionTitle.getText() ).toBe( 'Current Openings' );
  } );

  it( 'should have a jobs openings table ', function() {
    expect( page.jobOpeningsTable.isPresent() ).toBe( true );
  } );

  it( 'should have a career info section', function() {
    var infoSectionTitles =
    [ 'Job Application Process', 'Working at the CFPB' ];
    var infoSectionLinks =
    [ '/careers/application-process/', '/careers/working-at-cfpb/' ];

    expect( page.infoSectionTitles.getText() )
    .toEqual( infoSectionTitles );
    expect( page.infoSectionDescriptions.count() ).toEqual( 4 );
    expect( page.infoSectionLinks.getAttribute( 'href' ) )
    .toEqualUrl( infoSectionLinks );
  } );

  it( 'should have a social info section', function() {
    var socialSectionTitles = [ 'Follow us on LinkedIn',
    'Provide Feedback' ];
    var socialSectionLinks =
    [ 'https://www.linkedin.com/company/consumer-financial-protection-bureau',
    'mailto:jobs@consumerfinance.gov' ];

    expect( page.socialSectionTitles.getText() )
    .toEqual( socialSectionTitles );
    expect( page.socialSectionDescriptions.count() ).toEqual( 2 );
    expect( page.socialSectionLinks.getAttribute( 'href' ) )
    .toEqual( socialSectionLinks );
  } );

  it( 'should have a Related Links section', function() {
    expect( page.relatedLinksSection.isPresent() ).toBe( true );
  } );

} );
