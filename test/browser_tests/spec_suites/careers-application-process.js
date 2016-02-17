'use strict';

var ApplicationProcess = require(
    '../page_objects/page_careers-application-process.js'
  );

var Urlmatcher = require( '../util/url-matcher' );

describe( 'The Application Process Page', function() {
  var page;

  beforeAll( function() {
    page = new ApplicationProcess();
    page.get();

    jasmine.addMatchers( Urlmatcher );
  } );

  it( 'should properly load in a browser', function() {
    expect( page.pageTitle() ).toBe( 'Job Application Process' );
  } );

  it( 'should have a sideNav', function() {
    expect( page.sideNav.isPresent() ).toBe( true );
  } );

  it( 'should have an intro title', function() {
    expect( page.introSectionTitle.getText() )
    .toBe( 'Job Application Process' );
  } );

  it( 'should have three job application interfaces ', function() {
    expect( page.jobApplicationsInterfaces.count() ).toEqual( 3 );
  } );

  it( 'should have an ethics link ', function() {
    expect( page.ethicsLink.isPresent() ).toBe( true );
  } );

  it( 'should have a career info section', function() {
    var infoSectionTitles =
    [ 'Current Openings', 'Working at the CFPB',
    'Students & Recent Graduates' ];
    var infoSectionLinks =
    [ '/careers/current-openings/', '/careers/working-at-cfpb/',
    '/careers/students-and-graduates/' ];

    expect( page.infoSectionTitles.getText() )
    .toEqual( infoSectionTitles );
    expect( page.infoSectionDescriptions.count() ).toEqual( 5 );
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
