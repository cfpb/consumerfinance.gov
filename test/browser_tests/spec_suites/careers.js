'use strict';

var Careers = require(
    '../page_objects/page_careers.js'
  );

var Urlmatcher = require( '../util/url-matcher' );

describe( 'The Careers Page', function() {
  var page;

  beforeAll( function() {
    page = new Careers();
    page.get();

    jasmine.addMatchers( Urlmatcher );
  } );

  it( 'should properly load in a browser', function() {
    expect( page.pageTitle() ).toBe( 'Careers at the CFPB' );
  } );

  it( 'should have an intro title', function() {
    expect( page.introSectionTitle.getText() ).toBe( 'Careers at the CFPB' );
  } );

  it( 'should have an openings section', function() {
    expect( page.openingsSection.isPresent() ).toBe( true );
  } );

  it( 'should have a content sidebar', function() {
    expect( page.contentSidebar.isPresent() ).toBe( true );
  } );

  it( 'should have a career info section', function() {
    var infoSectionTitles = [ 'Job Application Process',
    'Students and Recent Graduates' ];
    var infoSectionLinks = [ '/careers/application-process/',
    '/careers/students-and-graduates/' ];

    expect( page.infoSectionTitles.getText() )
    .toEqual( infoSectionTitles );
    expect( page.infoSectionDescriptions.count() ).toEqual( 2 );
    expect( page.infoSectionLinks.getAttribute( 'href' ) )
    .toEqualUrl( infoSectionLinks );
  } );

  it( 'should have a career info section', function() {
    var infoSectionTitles = [ 'Job Application Process',
    'Students and Recent Graduates' ];
    var infoSectionLinks = [ '/careers/application-process/',
    '/careers/students-and-graduates/' ];

    expect( page.infoSectionTitles.getText() )
    .toEqual( infoSectionTitles );
    expect( page.infoSectionDescriptions.count() ).toEqual( 2 );
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

} );
